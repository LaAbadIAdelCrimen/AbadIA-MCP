import os
import json
from server.config import STORE_PATH

# Terminal colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
WHITE = "\033[37m"
RESET = "\033[0m"
FONDO_BLANCO = "\033[47m"

def load_map(map_name: str) -> list:
    """Loads a map from the storage directory."""
    path = os.path.join(STORE_PATH, f"{map_name}.json")
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

def save_map(map_name: str, map_data: list):
    """Saves a map to the storage directory."""
    path = os.path.join(STORE_PATH, f"{map_name}.json")
    with open(path, 'w') as f:
        json.dump(map_data, f, indent=4)

def draw_map_ascii(map_data: list, floor: int = 0, center_x: int = 5, center_y: int = 5, cells: int = 10) -> str:
    """
    Draws a portion of the map in ASCII using the compact format.
    """
    if not map_data or floor >= len(map_data):
        return "Map data is not available for this floor."

    floor_data = map_data[floor]
    output = ""
    
    min_y, max_y = center_y - cells, center_y + cells
    min_x, max_x = center_x - cells, center_x + cells

    for y in range(min_y, max_y):
        row_str = "{}|".format(format(y, '03d'))
        for x in range(min_x, max_x):
            if not (0 <= y < len(floor_data) and 0 <= x < len(floor_data[y])):
                if (y % 16) == 0 and (x % 16) == 0:
                    row_str += f"{GREEN}+{RESET}"
                else:
                    row_str += f"{WHITE}-{RESET}" 
                continue

            cell = floor_data[y][x]
            if cell is None:
                if (y % 16) == 0 and (x % 16) == 0:
                    row_str += f"{GREEN}+{RESET}"
                else:
                    row_str += f"{WHITE}-{RESET}" 
                continue

            char_id = cell.get("c", 0)
            obj_id  = cell.get("o", 0)
            height  = cell.get("h", 0)
            tmp = ""
            
            if height >= 16:
                tmp = "P"
            
            if height >= 0 and height < 12:
                tmp = f"{GREEN}.{RESET}"
            
            if height >= 12 and height < 16:
                tmp = f"{BLUE}{FONDO_BLANCO}#{RESET}"
            
            # Simplified character/object rendering for ASCII
            if obj_id > 0:
                tmp = f"{RED}O{RESET}"
            if char_id > 0:
                tmp = f"{YELLOW}C{RESET}"
            
            row_str += tmp
        output += row_str + "\n"

    return output
