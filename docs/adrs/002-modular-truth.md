# ADR-002: Modular Truth & The Vault Pattern

*   **Status:** Accepted
*   **Date:** 2026-05-16
*   **Context:** The project's documentation (README and SPECS) was becoming monolithic (> 500 lines), leading to "Context Rot" and agent hallucinations.

## Decision
We implement the **Index-Pointer Pattern** for all technical documentation and truth repositories.

1.  **Modular Specs:** All specifications are split into domain-specific files (movement, api, models) in `docs/specs/`, each strictly under 200 lines.
2.  **The Vault:** A dedicated infrastructure repository (`docs/vault/`) is established to store service contracts, standards, and security policies.
3.  **Cross-linking:** All modular files must be interlinked and indexed in a master `index.md`.

## Consequences
*   **Positive:** Higher agent legibility, reduced hallucinations, easier maintenance.
*   **Negative:** Increased number of files; requires strict indexing.
