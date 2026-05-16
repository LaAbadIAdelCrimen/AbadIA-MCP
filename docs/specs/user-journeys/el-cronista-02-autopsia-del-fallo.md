# Journey: el-cronista-02-autopsia-del-fallo

**Context:** Guillermo has been expelled (`haFracasado: true`).

## 1. Protocol
1. **Traceback:** Move back 5 actions from the `failure_tick`.
2. **Causal Anchor:** Identify the first sensory signal (Sound/Frase) that indicated a change in rule compliance.
3. **Hypothesis:** State the technical reason for failure (e.g., "Abbot collision due to lack of NOP waiting").
4. **Ratchet Proposal:** Suggest an update to the corresponding `user-journey` to prevent recurrence.

## 2. Verification & DoD
- **Implemented if:** The Chronicler correctly identifies the "Bell of Vespers" as the cause of an expulsion for being in the library.
- **DoD:** A failure report is saved in `storage/autopsies/`.
