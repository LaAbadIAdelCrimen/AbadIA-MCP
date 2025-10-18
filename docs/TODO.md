1. [x] create the map of the game
   (subtasks completed)
2. [x] Create a method to draw the map in ASCII.
   (subtasks completed)
3. [x] Fill the map with all data from the game state (rejilla, characters, objects, etc.).
   (subtasks completed)
4. [x] Modify the function `generate_default_map` to create 3 floors and a 400x400 array instead of 10x10.
5. [x] Prioritize loading `current_map.json` over `default_map.json` on startup.
   (subtasks completed)
6. [x] Implement auto-saving of the map when the player changes screens.
   (subtasks completed)
7. [x] Add a parameter to the `/map/ascii` endpoint to center the map on Guillermo.
   (subtasks completed)
8. [x] Centralize logger configuration and refactor its usage.
   (subtasks completed)
9. [x] Add detailed logging to the `/map/ascii` endpoint for debugging.
   (subtasks completed)
10. [x] Create API endpoints for loading and saving the game map.
    10.1. [ ] Create a `POST /map/save/{map_name}` endpoint in `server/main.py` that saves the current `game_map` to a file named `{map_name}.json` in the `storage` directory.
    10.2. [ ] Create a `POST /map/load/{map_name}` endpoint in `server/main.py` that loads the specified map file into the active `game_map`.