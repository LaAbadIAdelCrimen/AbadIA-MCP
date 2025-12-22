# Walkthrough: Movement Validation Logic

I have implemented the complex movement validation logic as specified in the updated `SPECS.md`. This ensures that Guillermo only moves to valid grid cells taking into account his volume, height constraints, and other characters.

## 1. Core Logic: `server/logic.py`

### Volume-Based Collision Detection
Implemented `check_volume_walkable` which checks a 5-cell pattern centered at the target position $(x, y)$:
- $(x, y)$
- $(x+1, y+1)$
- $(x-1, y-1)$
- $(x+1, y-1)$
- $(x-1, y+1)$

### Constraints
- **Height Delta**: The height of each of the 5 cells must be within $\pm 2$ of Guillermo's current height.
- **NPC Collisions**: I implemented `is_cell_occupied_by_any_character` which iterates over all NPCs and checks if their 5-cell volumes overlap with Guillermo's target volume.

### Move Calculation
`get_possible_moves_internal` calculates:
1.  **Cardinal Moves**: Iterates through N, NE, E, SE, S, SW, W, NW and validates each shift.
2.  **Basic Moves**: Maps the "Forward" cardinal direction (based on orientation) to the `UP` command. `LEFT` and `RIGHT` are included as they are assumed to be rotation-only.

## 2. API Exposure: `server/main.py`

- **MCP Tool**: Added `get_possible_moves()`.
- **FastAPI Route**: Added `GET /game/possible_moves`.

## 3. Verification Results

I created and ran a dedicated verification script `scripts/test_movement_logic.py` which mocks a scenario with a wall and an NPC blocking North.

**Test Output:**
```bash
Possible Moves result: {'status': 'OK', 'data': {'basic_moves': ['LEFT', 'RIGHT'], 'cardinal_moves': ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']}}
Basic Moves: ['LEFT', 'RIGHT']
Cardinal Moves: ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
SUCCESS: North is blocked as expected
```

## 4. Documentation

- Updated [BACKLOG.md](file:///Users/juantomas/proyectos/AbadIA-MCP/docs/BACKLOG.md) with Task 15.
- Updated [abadia_mcp.postman_collection.json](file:///Users/juantomas/proyectos/AbadIA-MCP/docs/abadia_mcp.postman_collection.json).

🍺
