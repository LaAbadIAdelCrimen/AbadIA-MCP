import sys
import os
import time
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Optional, Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure the root directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.logger_config import log
from server.common import ABADIA_SERVER_URL, sendCmd, session_id
from server.game_data import (
    save_game_status, 
    reset_game_data,
    initialize_map,
    get_game_map,
    get_game_status,
    load_game_map
)
from server.internal_game_data import get_internal_game_data
from server.map_utils import draw_map_ascii, save_map
from server.logic import (
    get_full_game_state_internal,
    send_game_command_internal,
    move_to_location_internal,
    investigate_location_internal,
    talk_to_character_internal,
    find_path_to_location_internal,
    get_possible_moves_internal
)

# Load environment variables
load_dotenv()

# --- Official MCP SDK Integration ---
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("AbadIA-MCP", instructions="Master Control Program for AbadIA System")

# Define MCP Tools using decorators
@mcp.tool()
async def move_to_location(location: str) -> str:
    """Moves Guillermo to a named location (e.g., 'library', 'church')."""
    res = move_to_location_internal(location)
    return res["message"]

@mcp.tool()
async def investigate_location(location: str) -> str:
    """Moves to and investigates a named location."""
    res = investigate_location_internal(location)
    return res["message"]

@mcp.tool()
async def talk_to_character(character: str) -> str:
    """Moves to and initiates conversation with a character."""
    res = talk_to_character_internal(character)
    return res["message"]

@mcp.tool()
async def get_full_game_state() -> Dict[str, Any]:
    """Retrieves the complete current game state JSON."""
    return get_full_game_state_internal()

@mcp.tool()
async def send_game_command(command: str) -> str:
    """Sends a low-level command like UP, DOWN, LEFT, RIGHT, SPACE."""
    send_game_command_internal(command)
    return f"Command {command} sent."

@mcp.tool()
async def find_path(dest_x: int, dest_y: int, floor: int = 0) -> str:
    """Calculates a path of commands to reaching specific coordinates."""
    res = find_path_to_location_internal(dest_x, dest_y, floor)
    if res["status"] == "OK":
        return f"Path found: {':'.join(res['data'])}"
    return f"Error: {res['message']}"
@mcp.tool()
async def get_possible_moves() -> Dict[str, Any]:
    """Calculates all possible moves (basic and cardinal) for Guillermo's current state."""
    return get_possible_moves_internal()


# --- FastAPI Application ---
app = FastAPI(
    title="AbadIA Dual Server",
    description="FastAPI + SSE MCP Official SDK Server",
    version="1.0.0"
)

# Mounting the MCP server (This enables SSE and other MCP routes)
# In many FastMCP versions, you can mount it directly or use its ASGI app.
# If FastMCP.mount() is available, we use it. Otherwise, we mount the ASGI.
# For simplicity in this common pattern:
# mcp.install(app) or similar if available, or just use SSE routes manually.
# FastMCP provides an ASGI app that we can mount.
app.mount("/mcp", mcp.sse_app())

@app.on_event("startup")
async def startup_event():
    log.info("Starting AbadIA Server...")
    initialize_map()

# --- Legacy REST API Endpoints ---

class GameResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

@app.get("/status", response_model=GameResponse, tags=["System"])
async def get_status():
    response = get_full_game_state_internal()
    if response is None:
        raise HTTPException(status_code=502, detail="Failed to communicate with game server")
    return GameResponse(status="OK", data=response, message="Status fetched successfully")

@app.get("/reset", response_model=GameResponse, tags=["System"])
async def reset_game():
    reset_game_data()
    initialize_map()
    sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='POST')
    time.sleep(1)
    sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='POST')
    response = sendCmd(ABADIA_SERVER_URL, "abadIA/game", mode='POST')
    save_game_status(response)
    return GameResponse(status="OK", data=response, message="Game reset successfully")

@app.get("/game/cmd/{cmd}", response_model=GameResponse, tags=["System"])
async def get_game_cmd(cmd: str):
    response = send_game_command_internal(cmd)
    if response is None:
        raise HTTPException(status_code=502, detail="Failed to communicate with game server")
    return GameResponse(status="OK", data=response, message=f"Command {cmd} execution attempted")

@app.get("/game/move/{cmd}", response_model=GameResponse, tags=["Movement"])
async def move_cardinal(cmd: str):
    # This logic still uses path2Pos for cardinal movement
    path2Pos = {
            "0N": "LEFT:UP:UP", "1N": "UP:UP", "2N": "RIGHT:UP:UP", "3N": "RIGHT:RIGHT:UP:UP",
            "0NE": "UP:UP:LEFT:UP:UP", "1NE": "UP:UP:RIGHT:UP:UP", "2NE": "RIGHT:UP:UP:RIGHT:UP:UP", "3NE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP",
            "0E": "UP:UP", "1E": "RIGHT:UP:UP", "2E": "RIGHT:RIGHT:UP:UP", "3E": "LEFT:UP:UP",
            "0SE": "UP:UP:RIGHT:UP:UP", "1SE": "RIGHT:UP:UP:RIGHT:UP:UP", "2SE": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP", "3SE": "UP:UP:LEFT:UP:UP",
            "0S": "RIGHT:UP:UP", "1S": "RIGHT:RIGHT:UP:UP", "2S": "LEFT:UP:UP", "3S": "UP:UP",
            "0SW": "RIGHT:UP:UP:RIGHT:UP:UP", "1SW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP", "2SW": "UP:UP:LEFT:UP:UP", "3SW": "UP:UP:RIGHT:UP:UP",
            "0W": "RIGHT:RIGHT:UP:UP", "1W": "LEFT:UP:UP", "2W": "UP:UP", "3W": "RIGHT:UP:UP",
            "0NW": "LEFT:UP:UP:LEFT:UP:UP", "1NW": "UP:UP:LEFT:UP:UP", "2NW": "UP:UP:RIGHT:UP:UP", "3NW": "RIGHT:RIGHT:UP:UP:RIGHT:UP:UP"
    }
    
    status_now = get_game_status()
    orientation = -1
    if status_now and 'Personajes' in status_now:
        guillermo = next((p for p in status_now['Personajes'] if p['nombre'] == 'Guillermo'), None)
        if guillermo: orientation = guillermo['orientacion']

    if orientation != -1:
        path_key = f"{orientation}{cmd}"
        if path_key in path2Pos:
            for command in path2Pos[path_key].split(':'):
                send_game_command_internal(command)
                time.sleep(0.1)
    
    new_status = get_full_game_state_internal()
    return GameResponse(status="OK", data=new_status, message=f"Moved {cmd}")

@app.get("/internal_status", tags=["System"])
def rest_internal_status():
    return get_internal_game_data()

@app.get("/map/ascii", tags=["Map"], response_class=PlainTextResponse)
def rest_map_ascii(floor: int = 0, center_x: int = 134, center_y: int = 170, cells: int = 20, center_on_guillermo: bool = True):
    game_map = get_game_map()
    if center_on_guillermo:
        st = get_game_status()
        if st and 'Personajes' in st:
            guillermo = next((p for p in st['Personajes'] if p['nombre'] == 'Guillermo'), None)
            if guillermo:
                center_x, center_y = guillermo['posX'], guillermo['posY']
    return draw_map_ascii(game_map, floor, center_x, center_y, cells)

@app.post("/map/save/{map_name}", tags=["Map"])
def rest_map_save(map_name: str):
    save_map(map_name, get_game_map())
    return {"status": "OK", "message": f"Saved {map_name}"}

@app.post("/map/load/{map_name}", tags=["Map"])
def rest_map_load(map_name: str):
    load_game_map(map_name)
    return {"status": "OK", "message": f"Loaded {map_name}"}

@app.post("/tools/move_to_location", tags=["Tools"])
def rest_tool_move(location: str):
    res = move_to_location_internal(location)
    if res["status"] == "ERROR": raise HTTPException(status_code=400, detail=res["message"])
    return res

@app.post("/tools/investigate_location", tags=["Tools"])
def rest_tool_investigate(location: str):
    res = investigate_location_internal(location)
    if res["status"] == "ERROR": raise HTTPException(status_code=400, detail=res["message"])
    return res

@app.post("/tools/talk_to_character", tags=["Tools"])
def rest_tool_talk(character: str):
    res = talk_to_character_internal(character)
    if res["status"] == "ERROR": raise HTTPException(status_code=400, detail=res["message"])
    return res

@app.post("/tools/find_path_to_location", response_model=GameResponse, tags=["Tools"])
async def find_path_to_location(dest_x: int, dest_y: int, floor: int = 0):
    res = find_path_to_location_internal(dest_x, dest_y, floor)
    if res["status"] == "OK":
        return GameResponse(status="OK", data=res["data"], message="Path found")
    else:
        return GameResponse(status="ERROR", message=res["message"])

@app.get("/game/possible_moves", response_model=GameResponse, tags=["Tools"])
async def get_possible_moves_endpoint():
    res = get_possible_moves_internal()
    if res["status"] == "OK":
        return GameResponse(status="OK", data=res["data"], message="Possible moves calculated")
    else:
        return GameResponse(status="ERROR", message=res["message"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
