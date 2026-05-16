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

## 4. Verification & Definition of Done (DoD)
A movement implementation is considered **Done** only if:
1. **Automated Unit Tests:** `tests/test_monastic_navigation.py` passes 100% of cases.
2. **Cardinal Accuracy:** Command sequences result in correct emulator orientation.
3. **Volume Integrity:** Guillermo never occupies a 1x1 gap.
