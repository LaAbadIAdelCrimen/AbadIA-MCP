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

## 4. Verification & DoD
1. **Schema Validation:** `scripts/validate_logs.py` must pass with 0 errors.
2. **Beyoncé Rule (Test):** `tests/test_logging_trigger.py` must prove that:
   - A command results in exactly one log entry.
   - A NOP command results in a state snapshot even if Guillermo is static.
3. **Storage Efficiency:** Logs must be rotated if they exceed 50MB.

---
*Status: Technical Contract | Ref: [[logging-refinery-spec]]*
