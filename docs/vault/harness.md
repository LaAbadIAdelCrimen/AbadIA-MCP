# Vault: Harness & Taskification Protocol

How to transform high-level requirements into autonomous build tasks.

## 1. The Spec-to-Task Loop (ST-Loop)
1. **Spec Identification:** Locate the modular spec in `docs/specs/`.
2. **ADR Link:** Verify the architectural decision in `docs/adrs/`.
3. **Task Decomposition:** Split the build into tasks < 50 lines of code change.
4. **Harness First:** Define the success criteria (tests) in the `TODO.md`.

## 2. The Ratchet Mechanism (Quality Control)
- **Standard:** If a task fails 3 times, it must be "demoted" back to a Research task in the Hub.
- **Refinement:** The agent must update the corresponding `docs/specs/` file with the pitfall found before attempting the task again.

## 3. Toolset Authorization
- Only tools registered in `vault/services.md` are authorized for execution.
- Ad-hoc scripts must live in `scripts/` and be documented in the Vault before use.

---
*Ref: [[harness-taskification-protocol]]*
