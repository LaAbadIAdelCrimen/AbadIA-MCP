import time
import heapq
from fastapi import HTTPException
from server.common import ABADIA_SERVER_URL, sendCmd
from server.logger_config import log
from server.game_data import (
    location_paths, 
    character_locations, 
    save_game_status,
    get_game_map,
    get_game_status,
    get_cell
)

def get_full_game_state_internal() -> dict:
    try:
        response = sendCmd(ABADIA_SERVER_URL, "abadIA/game/current", type="json", mode='GET')
        save_game_status(response)
        return response
    except Exception as e:
        log.error(f"Error getting full game state: {e}")
        return None

def send_game_command_internal(command: str) -> dict:
    try:
        response = sendCmd(ABADIA_SERVER_URL, f"abadIA/game/current/actions/{command}", mode='GET')
        save_game_status(response)
        return response
    except Exception as e:
        log.error(f"Error sending game command: {e}")
        return None

def move_to_location_internal(location: str) -> dict:
    if location not in location_paths:
        return {"status": "ERROR", "message": f"Location '{location}' not found."}

    try:
        path_commands = location_paths[location].split(':')
        for cmd in path_commands:
            send_game_command_internal(cmd)
            time.sleep(0.1)

        return {"status": "OK", "message": f"Successfully moved to {location}"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def investigate_location_internal(location: str) -> dict:
    res = move_to_location_internal(location)
    if res["status"] == "OK":
        send_game_command_internal("SPACE")
        return {"status": "OK", "message": f"Successfully investigated {location}"}
    return res

def talk_to_character_internal(character: str) -> dict:
    if character not in character_locations:
        return {"status": "ERROR", "message": f"Character '{character}' not found."}

    location = character_locations[character]
    res = move_to_location_internal(location)
    if res["status"] == "OK":
        send_game_command_internal("SPACE")
        return {"status": "OK", "message": f"Successfully talked to {character}"}
    return res

def find_path_to_location_internal(dest_x: int, dest_y: int, floor: int = 0) -> dict:
    game_map = get_game_map()
    game_status = get_game_status()

    if not game_status or 'Personajes' not in game_status:
        return {"status": "ERROR", "message": "Game status not available."}

    personajes = game_status['Personajes']
    guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)

    if not guillermo:
        return {"status": "ERROR", "message": "Guillermo not found."}

    start_x = guillermo['posX']
    start_y = guillermo['posY']

    path = a_star_search(game_map, floor, (start_x, start_y), (dest_x, dest_y))
    if not path:
        return {"status": "ERROR", "message": "Path not found."}

    commands = path_to_commands(path)
    return {"status": "OK", "data": commands}

# --- Pathfinding Helpers ---

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(game_map, floor, node, game_status, character_id, current_height):
    neighbors = []
    # N, S, E, W
    for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        x, y = node[0] + dx, node[1] + dy
        if check_volume_walkable(game_map, floor, x, y, current_height, character_id, game_status):
            neighbors.append((x, y))
    # Diagonal neighbors NE, SE, SW, NW
    for dx, dy in [(1, -1), (1, 1), (-1, 1), (-1, -1)]:
        x, y = node[0] + dx, node[1] + dy
        if check_volume_walkable(game_map, floor, x, y, current_height, character_id, game_status):
            neighbors.append((x, y))
    return neighbors

def a_star_search(game_map, floor, start, end):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    game_status = get_game_status()
    if not game_status:
        return None
    
    personajes = game_status.get('Personajes', [])
    guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)
    if not guillermo: return None
    gid = guillermo['id']
    gh = guillermo.get('altura', 0)

    while open_list:
        _, current = heapq.heappop(open_list)
        if current == end:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(game_map, floor, current, game_status, gid, gh):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [i[1] for i in open_list]:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    return None

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def path_to_commands(path):
    commands = []
    for i in range(len(path) - 1):
        dx = path[i+1][0] - path[i][0]
        dy = path[i+1][1] - path[i][1]
        if dx == 1: commands.append("RIGHT")
        elif dx == -1: commands.append("LEFT")
        elif dy == 1: commands.append("DOWN")
        elif dy == -1: commands.append("UP")
    return commands

# --- New Movement Validation Logic ---

def is_cell_occupied_by_any_character(x, y, floor, character_id, game_status):
    """
    Checks if a cell (x, y) is occupied by any character other than character_id.
    Each character occupies a 2x2 (or 3x3 pattern as per specs) volume.
    """
    if not game_status or 'Personajes' not in game_status:
        return False
    
    planta = game_status.get('Planta', 0)
    if planta != floor:
        return False

    for p in game_status['Personajes']:
        if p['id'] == character_id:
            continue
        
        px, py = p['posX'], p['posY']
        # Based on user spec: 2x2 volume
        p_volume = [
            (px, py),
            (px - 1, py),
            (px - 1, py + 1),
            (px, py + 1)
        ]
        if (x, y) in p_volume:
            return True
    return False

def check_volume_walkable(game_map, floor, x, y, current_height, character_id, game_status):
    """
    Checks if Guillermo's volume (2x2) can move to a new position (x, y).
    The cells are: (x, y), (x-1, y), (x-1, y+1), (x, y+1)
    """
    cells_to_check = [
        (x, y),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y + 1)
    ]
    for cx, cy in cells_to_check:
        # 1. Map boundaries
        if not (0 <= floor < len(game_map) and 0 <= cy < len(game_map[floor]) and 0 <= cx < len(game_map[floor][cy])):
            return False
        
        cell = game_map[floor][cy][cx]
        h = cell.get('h', 0) if cell else 0
        
        # 2. Height difference check (must be within +/- 2)
        if abs(h - current_height) > 2:
            return False
        
        # 3. Check for other characters
        if is_cell_occupied_by_any_character(cx, cy, floor, character_id, game_status):
            return False
            
    return True

def get_possible_moves_internal() -> dict:
    """
    Calculates the possible moves from the current position.
    Returns basic moves (UP, LEFT, RIGHT) and cardinal moves (N, NE, etc).
    """
    game_status = get_full_game_state_internal()
    if not game_status:
        return {"status": "ERROR", "message": "Could not fetch game status"}
    
    game_map = get_game_map()
    if not game_map:
        return {"status": "ERROR", "message": "Map not initialized"}

    personajes = game_status.get('Personajes', [])
    guillermo = next((p for p in personajes if p['nombre'] == 'Guillermo'), None)
    if not guillermo:
        return {"status": "ERROR", "message": "Guillermo not found"}

    gx, gy = guillermo['posX'], guillermo['posY']
    gh = guillermo.get('altura', 0)
    go = guillermo.get('orientacion', 0) # 0:E, 1:N, 2:W, 3:S
    floor = game_status.get('Planta', 0)
    gid = guillermo['id']

    cardinal_offsets = {
        "N": (0, -1), "NE": (1, -1), "E": (1, 0), "SE": (1, 1),
        "S": (0, 1), "SW": (-1, 1), "W": (-1, 0), "NW": (-1, -1)
    }

    possible_cardinal = []
    for direction, (dx, dy) in cardinal_offsets.items():
        if check_volume_walkable(game_map, floor, gx + dx, gy + dy, gh, gid, game_status):
            possible_cardinal.append(direction)

    # Basic moves: UP depends on orientation
    # Orientations: 0: E, 1: N, 2: W, 3: S
    orient_to_cardinal = {0: "E", 1: "N", 2: "W", 3: "S"}
    forward_cardinal = orient_to_cardinal[go]
    
    possible_basic = []
    if forward_cardinal in possible_cardinal:
        possible_basic.append("UP")
    
    # LEFT and RIGHT just change orientation, assume always possible for now
    possible_basic.append("LEFT")
    possible_basic.append("RIGHT")

    return {
        "status": "OK",
        "data": {
            "basic_moves": possible_basic,
            "cardinal_moves": possible_cardinal
        }
    }
