# Movement and Orientation Logic

## 1. Character Orientation
Orientation is tracked by an integer `0-3`:
- `0`: East (E)
- `1`: North (N)
- `2`: West (W)
- `3`: South (S)

## 2. Cardinal Movement Mapping (path2Pos)
To move in a cardinal direction, the system translates the target direction and current orientation into a sequence of low-level commands (`UP`, `LEFT`, `RIGHT`).

**Example: Target North (N)**
- Facing East (`0`): `LEFT:UP:UP`
- Facing North (`1`): `UP:UP`
- Facing West (`2`): `RIGHT:UP:UP`
- Facing South (`3`): `RIGHT:RIGHT:UP:UP`

*See `server/main.py` for the full mapping dictionary including NE, SE, SW, NW.*

## 3. The 2x2 Volume Rule
Guillermo and NPCs occupy a volume of 2x2 cells. A movement to `(x, y)` is only valid if:
1. All 4 cells are within map boundaries.
2. The height difference (`h`) for all 4 cells is `abs(h_target - h_current) <= 2`.
3. No cell is occupied by another character's volume.

**Cells in Volume:**
- `(x, y)`
- `(x-1, y)`
- `(x-1, y+1)`
- `(x, y+1)`

## 4. Verification & Validation (Detailed)

To verify the correct implementation of the movement logic, follow these steps:

1. **Static Validation (A* and Volume):**
   Run the movement logic test script:
   ```bash
   python3 scripts/test_movement_logic.py
   ```
   **Success Criteria:**
   - Output must show `SUCCESS: North is blocked by Wall` and `SUCCESS: East is blocked by Abbot`.
   - The cardinal moves list must exclude directions that violate the 2x2 volume rule.

2. **Functional Validation (Emulator Integration):**
   Run the functional server tests:
   ```bash
   pytest tests/test_functional_server.py
   ```
   **Success Criteria:**
   - `test_send_move_cmd_functional` must pass.
   - Verify that sending a move command (e.g., `GET /game/move/N`) results in the correct sequence of `UP`, `LEFT`, or `RIGHT` commands being sent to the emulator (observed in `logs/server.log`).

3. **In-Game Verification:**
   - Use the `get_possible_moves` tool via the MCP client.
   - Move Guillermo next to a character or a wall.
   - Verify that the tool correctly identifies the blocked direction.
