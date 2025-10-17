1. [x] create the map of the game
   1.1. [x] Define the JSON structure for the game map.
   1.2. [x] Create a module to handle map loading and saving from the `storage` directory.
   1.3. [x] Implement the logic to populate the map data (floors, coordinates, rooms, etc.).
   1.4. [x] Integrate the map module with the server's game state management.
2. [x] Create a method to draw the map in ASCII.
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
3. [x] Fill the map with all data from the game state (rejilla, characters, objects, etc.).
   3.1. [x] Create a new function `update_map_from_game_state(game_status)` in `server/game_data.py` which will be the main orchestrator for this process.
   3.2. [x] Inside this function, implement the logic to update the static map data (terrain and rooms) from the `rejilla`:
        - Extract key global data from `game_status`: `rejilla`, `personajes`, `objetos`, `planta` (the current floor), and `numPantalla` (the current room/screen number).
        - Find Guillermo's `posX` and `posY` to determine the player's absolute position.
        - Calculate the screen's top-left corner on the absolute map (`offsetX`, `offsetY`) using the formula: `(pos // 24) * 24`.
        - Loop through the 24x24 `rejilla`. For each cell, calculate its absolute `map_x` and `map_y`.
        - Access the correct cell in `game_map[planta][map_y][map_x]` and update its `height` with the value from the `rejilla` and its `room` with the `numPantalla`.
   3.3. [x] Create a helper function to update dynamic entities (characters and objects) on the map:
        - This function should first clear all existing `character` and `object` IDs from the current screen area on the `game_map` (using the calculated offsets and 24x24 size) to prevent entities from leaving trails.
        - Then, iterate through the `personajes` list from `game_status`. For each character, update the `character` ID in the `game_map` at their absolute `posX`, `posY` on the correct `planta`.
        - Do the same for the `objetos` list, updating the `object` ID for each item.
   3.4. [x] Modify the `save_game_status` function in `server/game_data.py`. Since this function is called immediately upon receiving any new game data from the server, it's the perfect trigger. It will be updated to call `update_map_from_game_state` to ensure our `game_map` is dynamically updated in real-time.
   3.5. [x] Create a comprehensive test script `scripts/test_map_update.py` and a corresponding `storage/sample_game_status.json` file. The script will:
        - Load the sample game status.
        - Call the `update_map_from_game_state` function.
        - Use `draw_map_ascii` to print the result, allowing us to visually verify that height, room number, characters, and objects are all placed correctly on the right floor.
4. [x] Modify the function `generate_default_map` to create 3 floors and a 400x400 array instead of 10x10.
5. [ ] Prioritize loading `current_map.json` over `default_map.json` on startup.
   5.1. [ ] Create a new function `initialize_map()` in `server/game_data.py`.
   5.2. [ ] Inside `initialize_map()`, implement the loading logic: check if `storage/current_map.json` exists. If yes, load "current_map"; if no, load "default_map". Add logging to indicate which map is being loaded.
   5.3. [ ] Modify the `startup_event` in `server/main.py` to call the new `initialize_map()` function instead of `load_game_map("default_map")`.
6. [ ] Implement auto-saving of the map when the player changes screens.
   6.1. [ ] Modify the `update_map_from_game_state` function in `server/game_data.py`.
   6.2. [ ] Before any updates are made, get the `numPantalla` from the incoming `game_status` and find Guillermo's `posX` and `posY`.
   6.3. [ ] Check the `room` number currently stored in `game_map` at Guillermo's position.
   6.4. [ ] If the new `numPantalla` is different from the stored `room` number (and the stored number is not 0), trigger a save by calling `save_map("current_map", game_map)`. Add logging to indicate that an auto-save has occurred due to a screen change.