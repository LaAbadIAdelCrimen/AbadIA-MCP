import sys
import os

# Add the parent directory to the sys.path to allow imports from the 'server' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.map_utils import save_map

def generate_default_map():
    """
    Generates a large, multi-floor default map (3 floors, 400x400 each) and saves it.
    """
    print("Generating large default map (3 floors, 400x400)...")
    
    map_data = []
    num_floors = 3
    width = 400
    height = 400

    for floor_num in range(num_floors):
        print(f"Generating floor {floor_num}...")
        floor = []
        for y in range(height):
            row = []
            for x in range(width):
                # Default cell data
                cell = {
                    "height": 0,
                    "character": 0,
                    "object": 0,
                    "room": 0
                }
                row.append(cell)
            floor.append(row)
        map_data.append(floor)

    print("Saving map to storage/default_map.json...")
    save_map("default_map", map_data)
    print("Default map saved successfully.")

if __name__ == "__main__":
    generate_default_map()