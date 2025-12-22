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
    get_game_status
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

def get_neighbors(game_map, floor, node):
    neighbors = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x, y = node[0] + dx, node[1] + dy
        if 0 <= x < len(game_map[floor][0]) and 0 <= y < len(game_map[floor]):
            cell = game_map[floor][y][x]
            if cell is None or cell.get('h', 0) < 16:
                neighbors.append((x, y))
    return neighbors

def a_star_search(game_map, floor, start, end):
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
