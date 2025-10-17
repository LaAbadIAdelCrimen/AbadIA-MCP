import sys
import os
import json

# Add the parent directory to the sys.path to allow imports from the 'server' module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.game_data import update_map_from_game_state, load_game_map, get_game_map
from server.map_utils import draw_map_ascii

def test_map_update():
    """
    Loads a sample game status, updates the map, and prints the result.
    """
    print("--- Starting Map Update Test ---")

    # Load the base map (e.g., the default 10x10 map)
    print("Loading base map...")
    load_game_map("default_map")

    # Load the sample game status
    print("Loading sample game status...")
    sample_status_path = "storage/sample_game_status.json"
    try:
        with open(sample_status_path, "r") as f:
            sample_status = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Could not find '{sample_status_path}'.")
        return

    # Run the update function
    print("Updating map from game status...")
    update_map_from_game_state(sample_status)

    # Get the updated map
    updated_map = get_game_map()

    # --- Verification ---
    print("\n--- Verifying Map Update ---")
    
    # Define the center for our ASCII view based on Guillermo's position
    guillermo = next((p for p in sample_status['personajes'] if p['nombre'] == 'Guillermo'), None)
    if not guillermo:
        print("ERROR: Guillermo not found in sample data.")
        return
        
    center_x = guillermo['posX']
    center_y = guillermo['posY']
    planta = sample_status['planta']

    print(f"Drawing map centered on Guillermo at ({center_x}, {center_y}) on floor {planta}")

    # Draw the map
    ascii_map = draw_map_ascii(
        map_data=updated_map,
        floor=planta,
        center_x=center_x,
        center_y=center_y,
        cells=15  # A radius of 15 to see the whole 24x24 screen
    )

    print(ascii_map)
    print("--- Test Complete ---")
    print("Check the output above to verify that 'G' (Guillermo), 'a' (Adso), and 'k' (key) are positioned correctly within the '#' walls.")


if __name__ == "__main__":
    test_map_update()
