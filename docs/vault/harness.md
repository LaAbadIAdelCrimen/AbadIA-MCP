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

## 4. HE v3.0 Iron Rules
- **No Plan without Spec:** Plans (PLN) cannot be generated if the corresponding Spec is incomplete or unverified by the human-in-the-loop.
- **Spec-to-Test Priority:** Every build task must start with a failing test derived directly from the Spec's "Verification" section.
- **The Human Escalation:** If a task remains failing after 3 Ratchet cycles, or if a Spec is ambiguous, the agent MUST pause and ask for human clarification.
- **Action-State Duality:** Every state change in the system MUST be traceable to an agent action (including NOP).

---
*Ref: [[harness-taskification-protocol]]*
