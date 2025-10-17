1. [x] create the map of the game
   1.1. [x] Define the JSON structure for the game map.
   1.2. [x] Create a module to handle map loading and saving from the `storage` directory.
   1.3. [x] Implement the logic to populate the map data (floors, coordinates, rooms, etc.).
   1.4. [x] Integrate the map module with the server's game state management.
2. [ ] Create a method to draw the map in ASCII.
   2.1. [ ] Implement the `draw_map_ascii(map_data, floor=0, center_x=134, center_y=170, cells=30)` function in `server/map_utils.py`.
   2.2. [ ] Create a test script `scripts/test_draw_map.py` that loads the `default_map` and uses the new function to print an ASCII representation to the console.
   2.3. [ ] Add a new API endpoint `GET /map/ascii` to `server/main.py` to expose the map drawing functionality.
