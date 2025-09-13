import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP
import requests
import logging
from agent.core.abadia_mcp import sendCmd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables with fallback values
ABADIA_SERVER_URL = os.getenv("ABADIA_SERVER_URL")
if not ABADIA_SERVER_URL:
    raise ValueError("ABADIA_SERVER_URL environment variable is not set.")

logger.info(f"ABADIA_SERVER_URL configured as: {ABADIA_SERVER_URL}")

# Example of how to use other environment variables with defaults
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
API_VERSION = os.getenv("API_VERSION", "1.0.0")


# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="AbadIA MCP Server",
    description="""
    Master Control Program (MCP) Server API for AbadIA system.
    
    ## Features
    * MCP command and control interface
 
    """,
    version="0.0.1",
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

class GameResponse(BaseModel):
    """Response model for game-related endpoints"""
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "OK",
                "data": {
                    "game_state": "reset",
                    "timestamp": "2024-03-21T10:00:00Z"
                },
                "message": "Game reset successfully"
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
    """
    return StatusResponse(status="OK")

@app.get(
    "/reset",
    response_model=GameResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
    summary="Reset AbadIA game",
    response_description="Reset AbadIA game status and response"
)
async def reset_game():
    """
    Reset AbadIA game.
    
    Returns:
        GameResponse with status and game data.
        If there's an error, returns appropriate error status.
    
    Example response:
        ```json
        {
            "status": "OK",
            "data": {
                "game_state": "reset", m 
                "timestamp": "2024-03-21T10:00:00Z"
            },
            "message": "Game reset successfully"
        }
        ```
    """
    try:
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='GET')
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='GET')
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server"
            )
        
        return GameResponse(
            status="OK",
            data=response if isinstance(response, dict) else {"raw_response": response},
            message="Game reset successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
       
@app.get(
    "/cmd/{cmd}",
    response_model=GameResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
    summary="send a command to AbadIA game",
    response_description="send a command to AbadIA game and get the status as response"
)
async def send_cmd(cmd: str):
    """
    send a command to AbadIA game.
    
    Args:
        cmd: The command to send (e.g., UP, DOWN, LEFT, RIGHT, SPACE, etc.)
    
    Returns:
        GameResponse with status and game data.
        If there's an error, returns appropriate error status.
    
    Example usage:
        GET /cmd/UP
        GET /cmd/DOWN
        GET /cmd/SPACE
    
    Example response:
        ```json
        {
            "status": "OK",
            "data": {
                "game_state": "command_executed",
                "timestamp": "2024-03-21T10:00:00Z"
            },
            "message": "Command UP sent successfully"
        }
        ```
    """
    try:
        response = sendCmd(ABADIA_SERVER_URL, f"abadIA/game/current/actions/{cmd}", mode='GET')
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server"
            )
        
        return GameResponse(
            status="OK",
            data=response if isinstance(response, dict) else {"raw_response": response},
            message=f"Command {cmd} sent successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
       



# MCP Configuration
mcp = FastApiMCP(
    app,
    name="AbadIA MCP Server",
    description="Master Control Program for AbadIA System",
)

# Mount MCP routes
mcp.mount()

from server.api.v1 import endpoints as v1_endpoints

app.include_router(v1_endpoints.router, prefix="/api/v1", tags=["v1"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)