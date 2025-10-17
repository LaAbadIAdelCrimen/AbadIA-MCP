import sys
import os

# Add the parent directory to the sys.path to allow imports from the 'server' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.map_utils import save_map

def generate_default_map():
    """
    Generates a default 10x10 map on a single floor and saves it.
    """
    print("Generating default map...")
    # Floor 0
    floor_0 = []
    for y in range(10):
        row = []
        for x in range(10):
            # Default cell data
            cell = {
                "height": 0,
                "character": 0,
                "object": 0,
                "room": 0
            }
            row.append(cell)
        floor_0.append(row)

    map_data = [floor_0] # The full map is a list of floors

    save_map("default_map", map_data)
    print("Default map saved to storage/default_map.json")

if __name__ == "__main__":
    generate_default_map()
