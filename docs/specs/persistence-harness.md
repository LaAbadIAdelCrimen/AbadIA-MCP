# Spec: Persistence Harness (The Scriptorium Vault)

This specification defines the mechanism for saving and restoring game states (Checkpoints). It allows the agent to maintain continuity across sessions and implement "Save-Scumming" as a strategic search technique.

## 1. Requirement: Session Persistence
The system must support the persistence of the full game state, including the grid, NPC positions, and monastic variables.
- **Save Operation:** Persists current state to a unique ID (e.g., `timestamp_goal_id`).
- **Load Operation:** Restores the emulator to a previously saved state ID.

## 2. The Rule of Perfect Grace (Zero Obsequium Loss)
- **Principle:** It is theoretically possible to complete the game without losing a single point of `obsequium`.
- **Constraint:** Any loss of `obsequium` indicates a "Validation Failure" in a previous journey.
- **Trigger:** If `obsequium_delta < 0`, the agent must immediately save the current state as a "Failure Node" and consider restoring a previous "Graceful State".

## 3. Data Schema (Checkpoints)
```json
{
  "checkpoint_id": "string",
  "obsequium": 31,
  "momentoDia": 4,
  "game_state": { ... },
  "metadata": {
    "last_journey": "string",
    "is_graceful": "bool"
  }
}
```

## 4. Verification & Validation (Detailed)
1. **Snapshot Test:**
   ```bash
   curl -s -X POST http://localhost:8000/map/save/test_session
   ls storage/test_session.json
   ```
   **Success:** The file must exist and contain a valid JSON state.

2. **Recovery Test:**
   - Move Guillermo.
   - Run: `curl -s -X POST http://localhost:8000/map/load/test_session`
   - Run: `GET /status`
   **Success:** Guillermo's coordinates must match the saved state.

---
*Standard: [[harness-standard-v3]] | Ref: [[persistence-harness]]*
