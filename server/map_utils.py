import json
import os

STORE_PATH = "store"

def load_map(map_name: str) -> list:
    """
    Loads a map from a JSON file in the store directory.

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
    Saves map data to a JSON file in the store directory.

    Args:
        map_name: The name of the map to save (without the .json extension).
        map_data: The map data to save.
    """
    if not os.path.exists(STORE_PATH):
        os.makedirs(STORE_PATH)
    map_path = os.path.join(STORE_PATH, f"{map_name}.json")
    with open(map_path, "w") as f:
        json.dump(map_data, f, indent=4)
