# Journey: el-cronista-01-tamizado-causal

**Context:** Session end. New log file in `storage/`.

## 1. Protocol
1. **Load:** Ingest the raw `.jsonl` entries.
2. **Material Check:** Filter out entries where Guillermo's position, NPCs, and sensory arrays remain identical to the previous tick.
3. **NOP Validation:** Ensure `NOP` commands that resulted in NPC movement are captured.
4. **Insight Extraction:** List all "Material Events" (New room, Item found, Sound heard).

## 2. Verification & DoD
- **Implemented if:** `scripts/validate_logs.py` shows a clean timeline of material events.
- **DoD:** A summary of the session's "Material Reality" is ready for the Ratchet update.
