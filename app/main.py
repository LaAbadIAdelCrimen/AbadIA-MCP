from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
from .api import router as api_router

# Load settings
settings = Settings()

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

@app.get("/")
async def root():
    return {"message": "Welcome to AbadIA-MCP Server"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 