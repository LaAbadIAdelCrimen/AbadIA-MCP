# Walkthrough: Movement Validation Logic

I have implemented the complex movement validation logic as specified in the updated `SPECS.md`. This ensures that Guillermo only moves to valid grid cells taking into account his volume, height constraints, and other characters.

## 1. Core Logic: `server/logic.py`

### 2x2 Square Volume Detection
Implemented the 2x2 volume check as per `SPECS.md`, centered at the current coordinates where $(x, y)$ is the Top-Right corner of the square:
- $(x, y)$
- $(x-1, y)$
- $(x-1, y+1)$
- $(x, y+1)$

### Bug Fix: Map Context
Fixed a bug in `check_volume_walkable` where it was incorrectly using the global `game_map` instead of the one passed during pathfinding/analysis. This ensures that the A* search and the `get_possible_moves` tool use the exact same validated physical constraints.

### Constraints
- **Height Delta**: Verified that $|height_{cell} - current\_height| \le 2$ is checked for all 4 cells.
- **NPC Collisions**: Improved `is_cell_occupied_by_any_character` to detect overlaps between the 2x2 volumes of Guillermo and any NPC.

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
