import json
import os
from server.map_definitions import CHARACTER_SYMBOLS, OBJECT_SYMBOLS
from server.ansi_colors import GREEN, RED, RESET, BLUE, YELLOW, WHITE
FONDO_BLANCO = "\033[47m"
FONDO_AZUL = "\033[44m"

STORE_PATH = "storage"

def _convert_and_compact_map(map_data: list) -> list:
    """
    Converts a map to the new compact format in place.
    - Replaces default empty cells with None.
    - Ensures keys are the new shortened versions.
    """
    default_old = {"height": 0, "character": 0, "object": 0, "room": 0}
    default_new = {"h": 0, "c": 0, "o": 0, "r": 0}

    for floor_idx, floor in enumerate(map_data):
        for y, row in enumerate(floor):
            for x, cell in enumerate(row):
                if cell == default_old or cell == default_new:
                    map_data[floor_idx][y][x] = None
                elif isinstance(cell, dict):
                    # Ensure keys are converted to the new format
                    if "height" in cell:
                        cell["h"] = cell.pop("height")
                    if "character" in cell:
                        cell["c"] = cell.pop("character")
                    if "object" in cell:
                        cell["o"] = cell.pop("object")
                    if "room" in cell:
                        cell["r"] = cell.pop("room")
    return map_data

def load_map(map_name: str) -> list:
    """
    Loads a map from a JSON file and converts it to the compact format.
    """
    map_path = os.path.join(STORE_PATH, f"{map_name}.json")
    if not os.path.exists(map_path):
        return []
    with open(map_path, "r") as f:
        map_data = json.load(f)
    
    return _convert_and_compact_map(map_data)

def save_map(map_name: str, map_data: list):
    """
    Saves map data to a JSON file in the storage directory.

    Args:
        map_name: The name of the map to save (without the .json extension).
        map_data: The map data to save.
    """
    if not os.path.exists(STORE_PATH):
        os.makedirs(STORE_PATH)
    map_path = os.path.join(STORE_PATH, f"{map_name}.json")
    with open(map_path, "w") as f:
        json.dump(map_data, f, indent=4)

def draw_map_ascii(map_data: list, floor: int = 0, center_x: int = 5, center_y: int = 5, cells: int = 10) -> str:
    """
    Draws a portion of the map in ASCII using the compact format.
    """
    from server.game_data import get_game_status
    if not map_data or floor >= len(map_data):
        return "Map data is not available for this floor."

    floor_data = map_data[floor]
    st = get_game_status()
    yy = 0
    output = ""
    
    min_y, max_y = center_y - cells, center_y + cells
    min_x, max_x = center_x - cells, center_x + cells

    for y in range(min_y, max_y):
        row_str = "{}|".format(format(y, '03d'))
        for x in range(min_x, max_x):
            if not (0 <= y < len(floor_data) and 0 <= x < len(floor_data[y])):
                if (y % 24) == 0 and (x % 24) == 0:
                    row_str += f"{GREEN}{"+"}{RESET}"
                else:
                    row_str += f"{WHITE}{"-"}{RESET}" 
                continue

            cell = floor_data[y][x]
            if cell is None:
                if (y % 24) == 0 and (x % 24) == 0:
                    row_str += f"{GREEN}{"+"}{RESET}"
                else:
                    row_str += f"{WHITE}{"-"}{RESET}" 
                continue

            char_id = cell.get("c", 0)
            obj_id  = cell.get("o", 0)
            height  = cell.get("h", 0)
            tmp = ""
            
            if height >= 16:
                tmp = "P"
            
            if height >= 0 and height < 12:
                tmp = f"{GREEN}{"."}{RESET}"
            
            if height >= 12 and height < 16:
                tmp = f"{BLUE}{FONDO_BLANCO}{"#"}{RESET}"
            
            if (y % 24) == 0 and (x % 24) == 0:
                tmp = f"{GREEN}{"+"}{RESET}"

            if char_id in CHARACTER_SYMBOLS:
                tmp = f"{YELLOW}{FONDO_AZUL}{CHARACTER_SYMBOLS[char_id]}{RESET}"

            if obj_id in OBJECT_SYMBOLS:
                tmp = tmp = f"{BLUE}{OBJECT_SYMBOLS[obj_id]}{RESET}"
            
            row_str += tmp
        row_str += "|" 
        # for x in range(min_x, max_x):
        for x in range(24):
            if yy in range(24):
                tmp = f"{GREEN}{format(st['Rejilla'][yy][x], '02x')}{RESET}"
            
                height =  st['Rejilla'][yy][x] % 16
                character = st['Rejilla'][yy][x] >> 4
                
                if height >= 0 and height < 12:
                    tmp = f"{GREEN}{format(height+character<<4, '02x')}{RESET}"
            
                if character >= 1: 
                    tmp = f"{YELLOW}{FONDO_AZUL}{format(height+(character<<4), '02x')}{RESET}"

                if height >= 12:
                    tmp = f"{BLUE}{FONDO_BLANCO}{format(height, '02x')}{RESET}"
                row_str += tmp

        output += row_str + "|\n"
        yy += 1
        
    return output
