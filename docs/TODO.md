7. [ ] Implement the `find_path_to_location` tool.
   7.1. [ ] Create a new endpoint `/tools/find_path_to_location` in `server/main.py`.
   7.2. [ ] Implement the pathfinding logic using the A* algorithm.
   7.3. [ ] The tool will take the destination coordinates as input and return a list of low-level commands.
   7.4. [ ] Create a new test script in the `scripts` directory to test the new tool.

8. [x] Refactor the game map to reduce space.
    8.1. [x] Change the keys in the map structure from {"height":0,"character":0,"object":0,"room":0} to {"h":0,"c":0,"o":0,"r":0}.
    8.2. [x] If a cell has the value {"h":0,"c":0,"o":0,"r":0}, substitute it for null.
    8.3. [x] Refactor every part of the code that interacts with the game map to check if a cell is null and, if so, act as if it were {"h":0,"c":0,"o":0,"r":0}.
    8.4. [x] Update all the code involved in the refactoring.

9. [x] Convert old map formats to the new compact format upon loading.
    9.1. [x] After loading a map, check for cells with default values.
    9.2. [x] If a cell is `{"h":0,"c":0,"o":0,"r":0}` or `{"height":0,"character":0,"object":0,"room":0}`, convert it to `None`.

10. [x] Create a global definition for ANSI color codes.
    10.1. [x] Create a new file for the color definitions.
    10.2. [x] Add the provided ANSI escape codes to the file.
    10.3. [x] Refactor the project to use the new color definitions.

11. [x] Implement map loading and truncation after game reset.
    11.1. [x] Modify the `reset_game` function in `server/main.py` to call a new map loading and processing function after `reset_game_data()`.
    11.2. [x] Create a new function in `server/game_data.py` (e.g., `initialize_and_truncate_map`) that handles the loading logic.
    11.3. [x] In this new function, implement the logic to load `current_map.json` if it exists, otherwise fall back to loading `default_map.json`.
    11.4. [x] After the map is loaded, add logic to truncate the map data:
        - Truncate the grid for `game_map[0]` to 256x256.
        - Truncate the grids for `game_map[1]` and `game_map[2]` to 100x100.
    11.5. [x] Review and confirm that the auto-save logic in `update_map_from_game_state` correctly saves the `game_map` to `current_map.json` whenever `numPantalla` changes.

12. [ ] Integrate Google ADK MCPtools for Server Access
    12.1. [ ] Analyze the existing `FastApiMCP` integration and determine the necessary changes to switch to `google.ai.generativelanguage` MCPtools.
    12.2. [ ] Refactor the server (`server/main.py`) to expose tools using the standard `google.ai.generativelanguage` library instead of the current custom implementation.
    12.3. [ ] Update the AI agent to use the new MCPtools for interacting with the server.
    12.4. [x] Create a simple Python script (`scripts/check_connection.py`) to verify the connection to the AbadIA MCP server's `/status` endpoint.
    12.5. [ ] Test the new integration to ensure all tools are correctly exposed and accessible.
