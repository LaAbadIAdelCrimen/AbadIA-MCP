from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP


# Load environment variables from .env file
load_dotenv()

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="AbadIA MCP Server",
    description="""
    Master Control Program (MCP) Server API for AbadIA system.
    
    ## Features
    * Real-time event monitoring
    * MCP command and control interface
    * System status and health checks
    * Event broadcasting and notifications
    
    ## Authentication
    This API requires an API key for secure operations.
    Set your API key in the .env file as `ABADIA_API_KEY`.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

class StatusResponse(BaseModel):
    """Response model for status endpoint"""
    status: str

    class Config:
        schema_extra = {
            "example": {
                "status": "OK"
            }
        }

@app.get(
    "/status",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
    summary="Get system status",
    response_description="System operational status"
)
async def get_status():
    """
    Retrieve AbadIA API status.
    
    Returns:
        JSONResponse with status "OK" if system is operational.
        Automatically returns 500 if there's an internal error.
    
    Example response:
        ```json
        {
            "status": "OK"
        }
        ```
    """
    return StatusResponse(status="OK")


# MCP Configuration
mcp = FastApiMCP(
    app,
    name="AbadIA MCP Server",
    description="Master Control Program for AbadIA System",
)

# Mount MCP routes
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)