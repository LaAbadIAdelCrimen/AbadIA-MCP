1. [x] create the map of the game
   1.1. [x] Define the JSON structure for the game map.
   1.2. [x] Create a module to handle map loading and saving from the `storage` directory.
   1.3. [x] Implement the logic to populate the map data (floors, coordinates, rooms, etc.).
   1.4. [x] Integrate the map module with the server's game state management.
2. [ ] Create a method to draw the map in ASCII.
   2.1. [x] In `server/game_data.py`, define mappings for characters and objects to their ASCII symbols (e.g., `CHARACTER_SYMBOLS = {1: 'G', 2: 'a'}`).
   2.2. [x] Implement the `draw_map_ascii` function in `server/map_utils.py`. This function will:
        - Take `map_data`, `floor`, `center_x`, `center_y`, and `cells` as input.
        - Calculate the drawing boundaries from the center and `cells` parameters.
        - Loop through the coordinates, building a string for each row.
        - For each cell, decide what to draw based on a priority: Character > Object > Terrain.
        - Use the height from the map data to represent terrain (e.g., height > 0 is a wall '#', height 0 is empty ' ').
        - Handle coordinates that are outside the map's boundaries (drawing them as void space).
        - Return a single multi-line string representing the map view.
   2.3. [x] Create a test script `scripts/test_draw_map.py` that:
        - Loads the `default_map.json`.
        - Manually adds a few characters and objects to the map data for testing purposes.
        - Calls `draw_map_ascii` and prints the result to the console to verify the visual output.
   2.4. [x] Add a new API endpoint `GET /map/ascii` to `server/main.py` that:
        - Accepts optional query parameters for `floor`, `center_x`, `center_y`, and `cells`.
        - Returns the ASCII map string within a JSON response, preserving formatting.