# PLN-001: Navigation Refactor (HE v3.0)

This plan implements Step 3 of the HE v3.0 cycle for the navigation system of abadIA.

## 1. Context & Anti-rationalization
- **Current State:** Navigation logic is spread across `logic.py` and `main.py`. Validation is partially implemented but lacks strict 2x2 volume enforcement in all tools.
- **Hypothesis:** By centralizing the **2x2 Volume Rule** and the **Cardinal Translation** in a deterministic Action Layer, the agent can navigate the Abbey with 0% collision rate.

## 2. Technical Contracts (Ref Vault/Specs)
- **Spec:** `docs/specs/movement.md` (2x2 Rule).
- **Service:** `vault/services.md` (MCP Tools).
- **Security:** `vault/security.md` (Obsequium Compliance).

## 3. Atomic Tasks

### [T-001] Harness: Navigation Baseline
- Create `tests/test_monastic_navigation.py`.
- **The Beyoncé Rule:** Implement tests for:
    - Path blocked by height (>2).
    - Path blocked by volume (2x2 corner collision).
    - Path blocked by NPC (Occupied cell).
- Status: Pending.

### [T-002] Build: Volume Validation Logic
- Refactor `server/logic.py`: `check_volume_walkable` to be the single source of truth.
- Update `get_neighbors` for pathfinding to use the refined check.
- Status: Pending.

### [T-003] Build: Cardinal Tool Integration
- Expose `get_possible_moves` as the primary tactical tool for the agent.
- Ensure `move_to_location` validates every step using the harness.
- Status: Pending.

## 4. Verification
- All tests in `tests/test_monastic_navigation.py` must pass.
- Agent Journey "Morning Recon" must be executable without manual intervention.

---
*Identity: Deterministic Navigation | Standard: HE v3.0*
