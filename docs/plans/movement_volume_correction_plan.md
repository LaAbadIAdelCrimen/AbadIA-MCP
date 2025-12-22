# Implementation Plan: Movement Volume and Cardinality Correction

This plan addresses the correction of the movement validation logic to strictly adhere to the 2x2 character volume and the 8 cardinal directions check.

## Proposed Changes

### [Component: Server Logic]

#### [MODIFY] [logic.py](file:///Users/juantomas/proyectos/AbadIA-MCP/server/logic.py)
- **Update Character Volume**: Change the 5-point cross pattern to the 2x2 square pattern: $(x, y), (x-1, y), (x-1, y+1), (x, y+1)$.
- **Verify Height Logic**: Ensure the $|height_{cell} - height_{Guillermo}| \le 2$ check is applied to all 4 cells.
- **Verify Cardinal Directions**: Ensure `get_possible_moves_internal` and `get_neighbors` correctly evaluate all 8 cardinal directions (N, NE, E, SE, S, SW, W, NW).

### [Component: Documentation]

#### [MODIFY] [BACKLOG.md](file:///Users/juantomas/proyectos/AbadIA-MCP/docs/BACKLOG.md)
- Add subtask 15.4 to reflect the 2x2 volume refinement.

## Verification Plan

### Automated Tests
- Update `scripts/test_movement_logic.py` to reflect the 2x2 volume.
- Add a specific test case for diagonal movement (NE) where a corner might block the 2x2 volume.

### Manual Verification
- Use the ASCII map to visually confirm that Guillermo cannot pass through 1-cell gaps if his 2x2 volume is blocked.
