import sys
import os

# Add the parent directory to the sys.path to allow imports from the 'server' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.map_utils import load_map, draw_map_ascii

def test_draw_map():
    """
    Loads the default map, adds some test characters/objects,
    and prints an ASCII representation to the console.
    """
    print("Loading default map for test...")
    map_data = load_map("default_map")

    if not map_data:
        print("Could not load default_map.json. Make sure it exists in the storage directory.")
        return

    # --- Modify map for testing ---
    # Place Guillermo (ID 1) at coordinates (y=5, x=5) on floor 0
    if len(map_data) > 0 and len(map_data[0]) > 5 and len(map_data[0][5]) > 5:
        map_data[0][5][5]["character"] = 1
        print("Placed Guillermo (G) at [0][5][5]")

    # Place a Key (ID 1) at coordinates (y=5, x=6) on floor 0
    if len(map_data) > 0 and len(map_data[0]) > 5 and len(map_data[0][5]) > 6:
        map_data[0][5][6]["object"] = 1
        print("Placed a Key (k) at [0][5][6]")
    
    # Make a wall (height > 0) at (y=4, x=5)
    if len(map_data) > 0 and len(map_data[0]) > 4 and len(map_data[0][4]) > 5:
        map_data[0][4][5]["height"] = 1
        print("Placed a wall (#) at [0][4][5]")
    # -----------------------------

    print("\n--- Drawing Map (Center: 5,5 | Radius: 5) ---")
    
    # Center the view on our new character
    ascii_map = draw_map_ascii(map_data, floor=0, center_x=5, center_y=5, cells=5)

    print(ascii_map)
    print("--- Test Complete ---")


if __name__ == "__main__":
    test_draw_map()
