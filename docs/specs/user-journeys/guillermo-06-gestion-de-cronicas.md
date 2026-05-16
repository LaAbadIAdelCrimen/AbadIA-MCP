# Journey: guillermo-06-gestion-de-cronicas

**Context:** Saving progress, restoring from failure, and ensuring monastic continuity.

## 1. Protocol
1. **Strategic Checkpoint:** Guillermo saves the state (`save_session`) before entering a high-risk area (e.g., Library at night or meeting the Abbot).
2. **Periodic Backup:** Automatically save every time a `momentoDia` changes or a goal is marked as `completed`.
3. **Grace Violation Recovery:** 
   - If `obsequium` drops, the journey is interrupted.
   - Guillermo evaluates the "Root Cause" using the Cronista.
   - Restore the last "Graceful State" (`load_session`) to try a different tactical approach.
4. **Session Handover:** On session start, the agent searches for the latest `checkpoint_id` and restores it.

## 2. Verification & Validation (Detailed)
1. **Auto-Save Verification:**
   - Execute a goal completion.
   - Check the `logs/checkpoint_audit.log`.
   **Success:** A new save entry must be present.

2. **Rollback Verification:**
   - Simulate a rule violation.
   - Trigger the `load_session` tool.
   **Success:** The `obsequium` in the next `GET /status` must be restored to its original value.

---
*Ref: [[persistence-harness]] | Persona: [[guillermo]]*
