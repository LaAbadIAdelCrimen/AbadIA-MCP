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
# abadia helpers 
# helper to normalize paths to positions
        #   1
        # 2   0
        #   3

path2Pos = {
            "0N": "LEFT:UP:UP",
            "1N": "UP:UP",
            "2N": "RIGHT:UP:UP",
            "3N": "RIGHT:RIGHT:UP:UP",

            "0NE": "UP:UP:LEFT:UP:UP",
            "1NE": "UP:UP:RIGHT:UP:UP",
            "2NE": "RIGHT:UP:UP:RIGHT:UP:UP",
            "3NE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",

            "0E": "UP:UP",
            "1E": "RIGHT:UP:UP",
            "2E": "RIGHT:RIGHT:UP:UP",
            "3E": "LEFT:UP:UP",

            "0SE": "UP:UP:RIGHT:UP:UP",
            "1SE": "RIGHT:UP:UP:RIGHT:UP:UP",
            "2SE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "3SE": "UP:UP:LEFT:UP:UP",

            "0S": "RIGHT:UP:UP",
            "1S": "RIGHT:RIGHT:UP:UP",
            "2S": "LEFT:UP:UP",
            "3S": "UP:UP",

            "0SW": "RIGHT:UP:UP:RIGHT:UP:UP",
            "1SW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "2SW": "UP:UP:LEFT:UP:UP",
            "3SW": "UP:UP:RIGHT:UP:UP",

            "0W": "RIGHT:RIGHT:UP:UP",
            "1W": "LEFT:UP:UP",
            "2W": "UP:UP",
            "3W": "RIGHT:UP:UP",

            "0NW": "LEFT:UP:UP:LEFT:UP:UP",
            "1NW": "UP:UP:LEFT:UP:UP",
            "2NW": "UP:UP:RIGHT:UP:UP",
            "3NW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP"

}

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
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='POST')
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='POST')
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
        response = sendCmd(ABADIA_SERVER_URL, f"abadIA/game/current/actions/{cmd}", mode='POST')
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
       

def sendCmd(url, command, type="json", mode="GET"):
        cmd = "{}/{}".format(url, command)
        try:
            if (type == "json"):
                headers = {'accept': 'application/json'}
            else:
                headers = {'accept': 'text/x.abadIA+plain'}

            if mode == "GET":
                r = requests.get(cmd)
            if mode == "POST":
                r = requests.post(cmd)
            logging.info(f"cmd ---> {cmd} {r.status_code}")
        except:
            logging.error(f"Vigasoco comm error {r.status_code}")
            return None
        headers = {'accept': 'text/x.abadIA+plain'}

        cmdDump = "{}/abadIA/game/current".format(url)
        core = requests.get(cmdDump, headers=headers)
        # logging.info(core.text)
        # core_dict =check2dict(core.text)

        headers = {'accept': 'application/json'}
        cmdDump = "{}/abadIA/game/current".format(url)
        r = requests.get(cmdDump, headers= headers)

        if (type == "json"):
            tmp = r.json()
            # tmp['core'] = core_dict

            if r.status_code == 599:
                tmp['haFracasado'] = True
            return tmp
        else:
            return r.text

def sendMultiCmd(path):
        logging.info("Path: %s Cmds: %s" % (path, path2Pos[path]))
        cmds = path2Pos[path].split(":")
        for step in cmds:
            sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/{}".format(step), mode='POST')

        headers = {'accept': 'text/x.abadIA+plain'}
        cmdDump = "{}/abadIA/game/current".format(ABADIA_SERVER_URL)
        core = requests.get(cmdDump, headers=headers)
        # logging.info(core.text)
        core_dict = check2dict(core.text)

        headers = {'accept': 'application/json'}
        cmdDump = "{}/abadIA/game/current".format(ABADIA_SERVER_URL)
        r = requests.get(cmdDump, headers=headers)
        tmp = r.json()
        tmp['core'] =  core_dict
        if r.status_code == 599:
            tmp['haFracasado'] = True
        return tmp

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