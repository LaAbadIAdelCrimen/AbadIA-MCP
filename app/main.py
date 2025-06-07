from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
from .api import router as api_router
from .mcp.server import mcp_server
import logging
import asyncio
from typing import Dict

# Load settings and configure logging
settings = Settings()
settings.setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AbadIA-MCP",
    description="MCP Server Implementation with FastAPI",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1", tags=["messages"])

@app.on_event("startup")
async def startup_event():
    """Start MCP server on application startup"""
    try:
        await mcp_server.start()
        logger.info("MCP server started successfully")
    except Exception as e:
        logger.error(f"Failed to start MCP server: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Stop MCP server on application shutdown"""
    try:
        await mcp_server.stop()
        logger.info("MCP server stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping MCP server: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AbadIA-MCP Server",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mcp_connections": len(mcp_server.connections),
        "uptime": "available"  # You could add actual uptime tracking here
    }

@app.get("/mcp/status")
async def mcp_status():
    """Get MCP server status"""
    return {
        "active_connections": len(mcp_server.connections),
        "server_host": settings.MCP_HOST,
        "server_port": settings.MCP_PORT,
        "max_connections": settings.MCP_MAX_CONNECTIONS
    }

@app.post("/mcp/broadcast")
async def broadcast_message(message: Dict):
    """Broadcast a message to all connected MCP clients"""
    try:
        await mcp_server.broadcast(message)
        return {"status": "success", "message": "Broadcast sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 