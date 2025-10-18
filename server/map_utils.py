import json
import os
from server.map_definitions import CHARACTER_SYMBOLS, OBJECT_SYMBOLS

STORE_PATH = "storage"

def load_map(map_name: str) -> list:
    """
    Loads a map from a JSON file in the storage directory.

    Args:
        map_name: The name of the map to load (without the .json extension).

    Returns:
        The map data as a list, or an empty list if the file doesn't exist.
    """
    map_path = os.path.join(STORE_PATH, f"{map_name}.json")
    if not os.path.exists(map_path):
        return []
    with open(map_path, "r") as f:
        return json.load(f)

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
    if not map_data or floor >= len(map_data):
        return "Map data is not available for this floor."

    floor_data = map_data[floor]
    output = ""
    
    min_y, max_y = center_y - cells, center_y + cells
    min_x, max_x = center_x - cells, center_x + cells

    for y in range(min_y, max_y):
        row_str = ""
        for x in range(min_x, max_x):
            if not (0 <= y < len(floor_data) and 0 <= x < len(floor_data[y])):
                row_str += " "
                continue

            cell = floor_data[y][x]
            if cell is None:
                row_str += "."  # Empty space is floor
                continue

            char_id = cell.get("c", 0)
            obj_id = cell.get("o", 0)
            height = cell.get("h", 0)

            if char_id in CHARACTER_SYMBOLS:
                row_str += CHARACTER_SYMBOLS[char_id]
            elif obj_id in OBJECT_SYMBOLS:
                row_str += OBJECT_SYMBOLS[obj_id]
            elif height > 0:
                row_str += "#"
            else:
                row_str += "."
        output += row_str + "\n"
        
    return output
