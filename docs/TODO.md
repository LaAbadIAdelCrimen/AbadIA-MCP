1. [x] create the map of the game
   (subtasks completed)
2. [x] Create a method to draw the map in ASCII.
   (subtasks completed)
3. [x] Fill the map with all data from the game state (rejilla, characters, objects, etc.).
   (subtasks completed)
4. [x] Modify the function `generate_default_map` to create 3 floors and a 400x400 array instead of 10x10.
5. [x] Prioritize loading `current_map.json` over `default_map.json` on startup.
   (subtasks completed)
6. [ ] Implement auto-saving of the map when the player changes screens.
   6.1. [ ] Modify the `update_map_from_game_state` function in `server/game_data.py`.
   6.2. [ ] Before any updates are made, get the `numPantalla` from the incoming `game_status` and find Guillermo's `posX` and `posY`.
   6.3. [ ] Get the `numPantalla` from the current `game_status` and compare it with the `room` number stored in the `game_map` at Guillermo's current position.
   6.4. [ ] If the new `numPantalla` is different from the stored `room` number (and the stored number is not 0), trigger a save by calling `save_map("current_map", game_map)`. Add logging to indicate that an auto-save has occurred due to a screen change.
7. [x] Add a parameter to the `/map/ascii` endpoint to center the map on Guillermo.
   (subtasks completed)
8. [x] Centralize logger configuration and refactor its usage.
   (subtasks completed)
9. [x] Add detailed logging to the `/map/ascii` endpoint for debugging.
   (subtasks completed)
10. [x] Create API endpoints for loading and saving the game map.
    (subtasks completed)
