import heapq
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.responses import JSONResponse, PlainTextResponse
from server.map_utils import draw_map_ascii, save_map
from fastapi import FastAPI, HTTPException, Query, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import httpx
import time
from dotenv import load_dotenv
from fastapi_mcp import FastApiMCP
import requests
from server.logger_config import log

# Correctly import from server.game_data
from server.game_data import (
    location_paths, 
    character_locations, 
    save_game_status, 
    reset_game_data,
    initialize_map,
    get_game_map,
    get_game_status,
    load_game_map
)
from server.internal_game_data import get_internal_game_data
from server.map_utils import draw_map_ascii

session_id = None

def sendCmd(url, command, type="json", mode="GET"):
        global session_id
        cmd = "{}/{}"
        headers = {}

        if session_id:
           headers['X-Session-Id'] = session_id

        if (type == "json"):
            headers['accept'] = 'application/json'
        else:
            headers['accept'] = 'text/x.abadIA+plain'

        try:
            if mode == "GET":
                r = requests.get(cmd.format(url, command), headers=headers)
            if mode == "POST":
                r = requests.post(cmd.format(url, command), headers=headers)
            log.info(f"cmd ---> {cmd.format(url, command)} {mode} {r.status_code} {r.json()}")

            if command == "abadIA/game" and r.status_code == 200:
               session_id = r.headers.get('X-Session-Id')
               log.info(f"New session ID: {session_id}")

        except requests.exceptions.RequestException as e:
            log.error(f"Vigasoco comm error: {e}")
            return None

        if (type == "json"):
            try:
                tmp = r.json()
                if r.status_code == 599:
                    tmp['haFracasado'] = True
                return tmp
            except ValueError:
                log.error("Failed to decode JSON from response")
                return None
        else:
            return r.text

# Get environment variables with fallback values
ABADIA_SERVER_URL = os.getenv("ABADIA_SERVER_URL")
if not ABADIA_SERVER_URL:
    raise ValueError("ABADIA_SERVER_URL environment variable is not set.")

log.info(f"ABADIA_SERVER_URL configured as: {ABADIA_SERVER_URL}")

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

@app.on_event("startup")
async def startup_event():
    """Initializes the map on server startup."""
    log.info("Initializing game map...")
    initialize_map()
    log.info("Map initialization complete.")


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
    operation_id="get_status",
    response_model=GameResponse,
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
    response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current", mode='GET')
    print(f"response ---> {response}")
    save_game_status(response)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to communicate with game server"
        )
        
    return GameResponse(
        status="OK",
        data=response if isinstance(response, dict) else {"raw_response": response},
        message="Game Status successfully"
    )
    
@app.get(
    "/reset",
    operation_id="reset_game",
    response_model=GameResponse,
    status_code=status.HTTP_200_OK,
    tags=["System"],
    summary="Reset AbadIA game",
    response_description="Reset AbadIA game status and response"
)
async def reset_game():
    """
    Resets the game by creating a new session and then sending reset commands.
    """
    global session_id
    session_id = None
    try:
        # Reset all internal MCP data first
        reset_game_data()
        initialize_map()

        # Create a new game, which is essential for getting a new session ID
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game", mode='POST')
        
        # Now, send the SPACE commands to navigate the game's main menu
        sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='POST')
        time.sleep(0.5) # A small delay can help prevent race conditions
        sendCmd(ABADIA_SERVER_URL, "abadIA/game/current/actions/SPACE", mode='POST')
        time.sleep(0.5)

        # Final status check
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current", mode='GET')
        save_game_status(response)

        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server after reset."
            )
        
        return GameResponse(
            status="OK",
            data=response,
            message="Game reset successfully"
        )
    except Exception as e:
        log.error(f"An error occurred during game reset: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
       
@app.get(
    "/game/cmd/{cmd}",
    operation_id="send_game_cmd",
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
    
        GET /game/cmd/UP
        GET /game/cmd/DOWN
        GET /game/cmd/SPACE
        GET /game/cmd/LEFT
        GET /game/cmd/RIGHT
    
    Valid cmd are: LEFT, RIGHT, UP, DOWN, SPACE

    UP is for going a step ahead.
    LEFT is just for turn left.
    RIGHT is just for turn right.
    DOWN for picking an object.

When you want to make an step need to send UP twice. 
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
        print(f"response CMD --> ({response})")
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current", mode='GET')
        print(f"response ---> {response}")
        save_game_status(response)
        if response is None:
            raise HTTPException (
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
       
@app.get("/internal_status", operation_id="get_internal_status", tags=["System"])
def get_internal_status_data():
    """
    Returns the server's internal representation of the game state.
    This is useful for debugging and understanding the AI's perspective.
    """
    return get_internal_game_data()

@app.get("/map", operation_id="get_map", tags=["System"])
def get_map_data():
    """
    Returns the currently loaded game map.
    """
    return get_game_map()

from server.game_data import get_game_status

@app.get("/map/ascii", operation_id="get_map_ascii", tags=["System"], response_class=PlainTextResponse)
def get_map_ascii_data(
    floor: int = 0, 
    center_x: int = 134, 
    center_y: int = 170, 
    cells: int = 30,
    center_on_guillermo: bool = True
):
    """
    Returns an ASCII representation of the current game map.
    """
    game_map = get_game_map()
    
    # If requested, center the map on Guillermo's current position
    if center_on_guillermo:
        game_status = get_game_status()
        if game_status and 'Personajes' in game_status:
            personajes = game_status['Personajes']
            guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)
            if guillermo:
                center_x = guillermo['posX']
                center_y = guillermo['posY']
                log.info(f"Centering map on Guillermo at ({center_x}, {center_y}).")
            else:
                log.warning("'center_on_guillermo' is True, but Guillermo was not found in the current game status.")
                log.warning(f"Full game status for debugging: {game_status}")
        else:
            log.warning("'center_on_guillermo' is True, but no game status or 'Personajes' list is available.")

    log.info(f"Generating ASCII map with parameters: floor={floor}, center_x={center_x}, center_y={center_y}, cells={cells}.")
    return draw_map_ascii(
        map_data=game_map,
        floor=floor,
        center_x=center_x,
        center_y=center_y,
        cells=cells
    )

from server.map_utils import save_map

@app.post("/map/save/{map_name}", operation_id="save_map", tags=["System"])
def save_map_data(map_name: str):
    """
    Saves the current in-memory game map to a file in the 'storage' directory.
    """
    log.info(f"Received request to save current map to '{map_name}.json'.")
    game_map = get_game_map()
    save_map(map_name, game_map)
    return {"status": "OK", "message": f"Map successfully saved to {map_name}.json"}

@app.post("/map/load/{map_name}", operation_id="load_map", tags=["System"])
def load_map_data(map_name: str):
    """
    Loads a map from a file in the 'storage' directory into the active in-memory map.
    """
    log.info(f"Received request to load map '{map_name}.json' into memory.")
    load_game_map(map_name)
    return {"status": "OK", "message": f"Map '{map_name}.json' loaded into memory."}

@app.post("/tools/move_to_location", operation_id="move_to_location")
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

@app.post("/tools/investigate_location", operation_id="investigate_location")
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

@app.post("/tools/talk_to_character", operation_id="talk_to_character")
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

@app.get("/tools/get_full_game_state", operation_id="get_full_game_state")
def get_full_game_state() -> dict:
    """
    Gets the complete current state of the game from the MCP server,
    including character position, time, inventory, etc.
    """
    try:
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current", type="json", mode='GET')
        save_game_status(response)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server"
            )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/send_game_command", operation_id="send_game_command")
def send_game_command(command: str) -> dict:
    """
    Sends a single, low-level command to the game (e.g., 'UP', 'DOWN', 'SPACE').
    Use this for fine-grained control when high-level actions are not precise enough.
    """
    try:
        response = sendCmd(ABADIA_SERVER_URL, f"abadIA/game/current/actions/{command}", mode='GET')
        save_game_status(response)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to communicate with game server"
            )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/find_path_to_location", operation_id="find_path_to_location")
def find_path_to_location(dest_x: int, dest_y: int, floor: int = 0) -> dict:
    """
    Finds a path from the character's current location to a destination.
    This is a high-level action that may take some time.
    """
    game_map = get_game_map()
    game_status = get_game_status()

    if not game_status or 'Personajes' not in game_status:
        raise HTTPException(status_code=409, detail="Game status not available.")

    personajes = game_status['Personajes']
    guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)

    if not guillermo:
        raise HTTPException(status_code=409, detail="Guillermo not found.")

    start_x = guillermo['posX']
    start_y = guillermo['posY']

    path = a_star_search(game_map, floor, (start_x, start_y), (dest_x, dest_y))

    if not path:
        raise HTTPException(status_code=404, detail="Path not found.")

    commands = path_to_commands(path)

    return {"status": "OK", "data": commands, "message": "Path found successfully."}


def a_star_search(game_map, floor, start, end):
    """
    A* pathfinding algorithm.
    """
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(game_map, floor, current):
            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [i[1] for i in open_list]:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None


def heuristic(a, b):
    """
    Heuristic function for A*.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(game_map, floor, node):
    """
    Get neighbors of a node, compatible with compact map format.
    """
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < len(game_map[floor][0]) and 0 <= y < len(game_map[floor]):
            cell = game_map[floor][y][x]
            # A cell is navigable if it's None (empty) or its height is less than 16.
            if cell is None or cell.get('h', 0) < 16:
                neighbors.append((x, y))
    return neighbors


def reconstruct_path(came_from, current):
    """
    Reconstruct path from came_from map.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]


def path_to_commands(path):
    """
    Convert a path to a list of commands.
    """
    commands = []
    for i in range(len(path) - 1):
        dx = path[i+1][0] - path[i][0]
        dy = path[i+1][1] - path[i][1]
        if dx == 1:
            commands.append("RIGHT")
        elif dx == -1:
            commands.append("LEFT")
        elif dy == 1:
            commands.append("DOWN")
        elif dy == -1:
            commands.append("UP")
    return commands

# MCP Configuration
mcp = FastApiMCP(
    app,
    name="AbadIA MCP Server",
    description="Master Control Program for AbadIA System",
)

# Mount MCP routes
mcp.mount_http()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
