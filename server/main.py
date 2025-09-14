import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def sendCmd(url, command, type="json", mode="GET"):
        cmd = "{}/{}"
        try:
            if (type == "json"):
                headers = {'accept': 'application/json'}
            else:
                headers = {'accept': 'text/x.abadIA+plain'}

            if mode == "GET":
                r = requests.get(cmd.format(url, command))
            if mode == "POST":
                r = requests.post(cmd.format(url, command))
            logging.info(f"cmd ---> {cmd} {r.status_code}")
        except:
            logging.error(f"Vigasoco comm error {r.status_code}")
            return None
        headers = {'accept': 'text/x.abadIA+plain'}

        cmdDump = "{}/abadIA/game/current"
        core = requests.get(cmdDump.format(url), headers=headers)

        headers = {'accept': 'application/json'}
        cmdDump = "{}/abadIA/game/current"
        r = requests.get(cmdDump.format(url), headers= headers)

        if (type == "json"):
            tmp = r.json()

            if r.status_code == 599:
                tmp['haFracasado'] = True
            return tmp
        else:
            return r.text

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
    Model Control Program (MCP) Server API for AbadIA system.
    
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
        json_schema_extra = {
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
        json_schema_extra = {
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
    "/game/cmd/{cmd}",
    response_model=GameResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
    summary="send a command to AbadIA game",
    response_description="send a command to AbadIA game and get the status as response"
)
async def send_game_cmd(cmd: str):
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
       



from server.game_data import location_paths, character_locations
import time

@app.post("/tools/move_to_location")
def move_to_location(location: str) -> dict:
    """
    Moves the character to a named location in the abbey (e.g., 'library', 'church').
    This is a high-level action that may take some time.
    """
    if location not in location_paths:
        raise HTTPException(status_code=404, detail=f"Location '{location}' not found.")

    try:
        path_commands = location_paths[location].split(':')
        for cmd in path_commands:
            send_game_command(cmd)
            time.sleep(0.1)

        final_state = get_full_game_state()

        return {"status": "OK", "data": final_state, "message": f"Successfully moved to {location}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/investigate_location")
def investigate_location(location: str) -> dict:
    """
    Moves to and investigates a named location in the abbey (e.g., 'library', 'church').
    Use this to search for clues or interact with the environment.
    """
    try:
        move_to_location(location)
        send_game_command("SPACE")
        final_state = get_full_game_state()
        return {"status": "OK", "data": final_state, "message": f"Successfully investigated {location}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/talk_to_character")
def talk_to_character(character: str) -> dict:
    """
    Moves to a character and initiates a conversation (e.g., 'abbot', 'jorge').
    """
    if character not in character_locations:
        raise HTTPException(status_code=404, detail=f"Character '{character}' not found.")

    try:
        location = character_locations[character]
        move_to_location(location)
        send_game_command("SPACE")
        final_state = get_full_game_state()
        return {"status": "OK", "data": final_state, "message": f"Successfully initiated conversation with {character}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/get_full_game_state")
def get_full_game_state() -> dict:
    """
    Gets the complete current state of the game from the MCP server,
    including character position, time, inventory, etc.
    """
    try:
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current", type="json", mode='GET')
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server"
            )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/send_game_command")
def send_game_command(command: str) -> dict:
    """
    Sends a single, low-level command to the game (e.g., 'UP', 'DOWN', 'SPACE').
    Use this for fine-grained control when high-level actions are not precise enough.
    """
    try:
        response = sendCmd(ABADIA_SERVER_URL, f"abadIA/game/current/actions/{command}", mode='GET')
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server"
            )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# MCP Configuration
mcp = FastApiMCP(
    app,
    name="AbadIA MCP Server",
    description="Master Control Program for AbadIA System",
)

# Mount MCP routes
mcp.mount_http()

from server.api.v1 import endpoints as v1_endpoints

app.include_router(v1_endpoints.router, prefix="/api/v1", tags=["v1"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)