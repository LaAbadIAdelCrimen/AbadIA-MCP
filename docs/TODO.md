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

10. [ ] Create a global definition for ANSI color codes.
    10.1. [x] Create a new file for the color definitions.
    10.2. [x] Add the provided ANSI escape codes to the file.
    10.3. [ ] Refactor the project to use the new color definitions.