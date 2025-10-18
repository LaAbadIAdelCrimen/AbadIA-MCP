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
   9.1. [ ] Modify the `get_map_ascii_data` function in `server/main.py`.
   9.2. [ ] If `center_on_guillermo` is true and Guillermo is found, log his name and the coordinates being used as the center.
   9.3. [ ] If Guillermo is *not* found, log a warning and also log the entire `game_status` content to help with debugging why he is missing.
   9.4. [ ] Log the final parameters (floor, center_x, center_y, cells) that are being passed to the `draw_map_ascii` function.
