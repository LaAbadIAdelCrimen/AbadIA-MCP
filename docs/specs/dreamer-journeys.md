# Dreamer Journeys: The Nightly Review

Protocols for the Chronicler to analyze the day's events in the Abbey.

## 1. Journey: "The Causal Sieve" (El Tamizado Causal)
**Context:** Session end. A new log file exists in `storage/`.
1. **Load:** Ingest the raw `.jsonl` entries.
2. **Action-State Alignment:** For each entry `n`, identify the action taken by Guillermo and compare State `n` with State `n+1`.
3. **Delta Detection:** If `State(n+1) != State(n)`, flag as "Material Change".
4. **NOP Validation:** Explicitly verify that a `NOP` command resulted in an emulator tick and capture the state of NPCs (who move even if Guillermo doesn't).

## 2. Journey: "The Failure Autopsy" (Autopsia del Error)
**Context:** Guillermo has been expelled (`haFracasado: true`).
1. **Traceback:** Move back 5 actions from the failure.
2. **Sensor Check:** Identify the first occurrence of a "Danger Sensor" (Abbot proximity, specific Sound ID).
3. **Hypothesis:** Formulate why the failure occurred (e.g., "Guillermo did not react to Sound ID 4 within 3 ticks").

## 3. Verification & DoD
- **Delta Accuracy:** 100% of material state changes are captured.
- **Tick Continuity:** No gaps in the sequence of actions.
- **Report Generation:** The journey results in a "Experience Report" suitable for the **Ratchet** mechanism.

---
*Status: Dreamer Protocols | Ref: [[dreamer-journeys]]*
