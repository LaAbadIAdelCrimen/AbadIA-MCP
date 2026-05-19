# SPEC: Monastic Navigation & Map Services
Status: Draft
Version: 1.0.0
Role: Contract for deterministic movement and map rendering.

## 1. Overview
This specification defines the validation requirements for pathfinding, movement constraints, and map rendering in the AbadIA-MCP system. Following the **Beyoncé Rule**, these tests must pass before the Complexity Ratchet is armed.

## 2. Functional Requirements

### A. Map Services (`server/map_utils.py`)
- **Requirement 1:** Load maps from JSON files in the storage directory.
- **Requirement 2:** Save map state to persistent JSON files.
- **Requirement 3:** Render an ASCII view of the map centered on a coordinate or character.
- **Validation Proofs (Tests):**
  - `test_load_map_success`: Load an existing map.
  - `test_load_map_not_found`: Return empty list for missing map.
  - `test_save_map`: Verify file creation and JSON structure.
  - `test_draw_map_ascii_rendering`: Verify colors and symbols (P, ., #, O, C) are correctly placed.

### B. Navigation Logic (`server/logic.py`)
- **Requirement 4:** A* Pathfinding between two points on the same floor.
- **Requirement 5:** Volume validation (2x2) for Guillermo's movement.
- **Requirement 6:** Height difference constraint (max +/- 2).
- **Requirement 7:** Character collision detection.
- **Validation Proofs (Tests):**
  - `test_a_star_path_found`: Valid path between two adjacent cells.
  - `test_a_star_no_path`: Blocked destination returns None.
  - `test_check_volume_walkable_success`: 2x2 area is clear.
  - `test_check_volume_walkable_blocked_height`: 2x2 area has height difference > 2.
  - `test_check_volume_walkable_blocked_collision`: 2x2 area is occupied by another character.
  - `test_is_cell_occupied`: Correctly identifies character positions based on game state.

## 3. Coverage Target
- Minimum 90% for `server/logic.py`.
- Minimum 90% for `server/map_utils.py`.

---
*Standard: HE v3.0 | Identity: Adso/Guillermo*
