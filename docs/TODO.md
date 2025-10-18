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
7. [ ] Add a parameter to the `/map/ascii` endpoint to center the map on Guillermo.
   7.1. [ ] Modify the `get_map_ascii_data` function in `server/main.py` to accept a new boolean query parameter `center_on_guillermo`, defaulting to `True`.
   7.2. [ ] Inside the function, if `center_on_guillermo` is `True`, find Guillermo in the current `game_status` to get his `posX` and `posY`.
   7.3. [ ] If Guillermo is found, use his coordinates as the `center_x` and `center_y` for the `draw_map_ascii` function call, overriding any other parameters. If he is not found, fall back to the default center coordinates.
