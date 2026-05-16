# ADR-005: Autonomous Planning Engine (ST-Loop)

*   **Status:** Proposed
*   **Date:** 2026-05-16
*   **Context:** Currently, the agent's planning is done via a single large prompt. This is prone to alucinations and lacks determinism. We need a way to break down "Goals" into "Tasks" using the "Vault" as the technical oracle.

## Decision
We implement the **ST-Loop (Spec-to-Task)** as a multi-stage process:

1.  **Spec Analyzer:** Reads `goals.md` and identifies the current milestone.
2.  **Vault Oracle:** Queries `docs/vault/services.md` and `docs/vault/security.md` to identify available tools and constraints for that milestone.
3.  **Taskifier:** Generates a `tasks.json` file with atomic operations (< 20 lines of code logic per task if code is involved).
4.  **Harness Validator:** Every task must be preceded by a test case in `tests/`.

## Consequences
*   **Positive:** Highly deterministic behavior, traceability from goal to code, and automatic error recovery via the Ratchet mechanism.
*   **Negative:** Higher initial overhead in plan generation.
