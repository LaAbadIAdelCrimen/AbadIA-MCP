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
8. [ ] Centralize logger configuration and refactor its usage.
   8.1. [x] Create a new file `server/logger_config.py` to house the global logger setup.
   8.2. [x] In this new file, configure a single, project-wide logger (e.g., named "AbadIA") with a consistent format and level (INFO).
   8.3. [x] In `server/main.py`, remove the local logger setup and instead import the configured logger from `server.logger_config`.
   8.4. [x] In `server/game_data.py`, remove the local logger setup and import the global logger as well.
   8.5. [ ] Go through both `server/main.py` and `server/game_data.py` and ensure all logging calls use the new, imported global logger.