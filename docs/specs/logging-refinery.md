# Spec: Logging Refinery (The Chronicler's Ink)

This specification defines the technical contract for the new logging system, ensuring the Dreamer has high-quality data to analyze.

## 1. Requirement: Action-Triggered Capture
The system must capture a snapshot of the game state **before and after** every action sent to the emulator.
- **Trigger:** Any call to `send_game_command` (including a dedicated `NOP` command).
- **Format:** JSONL (JSON Lines) to ensure atomicity and crash-resilience.

## 2. Log Entry Schema
Each line must contain:
```json
{
  "timestamp": "ISO8601",
  "action": "UP|DOWN|LEFT|RIGHT|SPACE|NOP",
  "goal_id": "string (from goals.md)",
  "state_before": { ... },
  "state_after": { ... },
  "delta": {
    "pos_changed": "bool",
    "sensory_events": ["list of sound/phrase IDs"]
  }
}
```

## 3. The NOP Rule
- **Definition:** A NOP (No Operation) command must be sent if the agent needs to wait.
- **Impact:** The log must capture how NPCs move during that NOP tick.

## 4. Verification & Validation (Detailed)

To verify the Logging Refinery implementation:

1. **Trigger Validation:**
   Execute a command and check the log file:
   ```bash
   curl -s http://localhost:8000/game/cmd/UP
   tail -n 1 logs/game_trajectory.jsonl | jq .
   ```
   **Success Criteria:**
   - A new line is appended to the log.
   - The `action` field matches the command sent.
   - Both `state_before` and `state_after` are populated and different (if Guillermo moved).

2. **NOP Rule Test:**
   Run the NOP validation script:
   ```bash
   python3 scripts/st_loop.py --nop-only --ticks 5
   ```
   **Success Criteria:**
   - The log must contain 5 entries.
   - The entries must show NPC movements in `state_after` while Guillermo's position remains constant in `state_before` and `state_after`.

3. **Schema Compliance:**
   Run the log validator:
   ```bash
   python3 scripts/validate_logs.py
   ```
   **Success Criteria:**
   - 0 errors reported for the current `game_trajectory.jsonl`.

---
*Status: Technical Contract | Ref: [[logging-refinery-spec]]*
