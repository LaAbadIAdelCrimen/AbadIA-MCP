# AGENTS.md — abadIA Autonomous Operations Manual (HE v3.0)

This is the canonical source of truth for all autonomous agents (Gemini-cli, Antigravity/Honcho, Claude Code, Hermes) operating on the abadIA project.

## 1. The Rule of Perfect Grace
**Zero Obsequium Loss Goal:** It is possible to complete the game with 100% obsequium. 
- If `obsequium` decreases, a plan has failed retrospective validation.
- Agents must use the **Persistence Harness** to save state before risky actions and rollback on failure.

## 2. Naming Conventions & Relationships
To ensure HE validation, all documentation must follow this schema:

### A. Specifications (`docs/specs/*.md`)
- **Name:** `[system-component].md` (e.g., `movement.md`, `persistence-harness.md`).
- **Role:** The **Contract**. Defines the "What" and "Validation Proofs."
- **Relation:** Must list the User Journeys that implement it.

### B. User Journeys (`docs/specs/user-journeys/*.md`)
- **Name:** `[persona]-[id]-[action].md` (e.g., `guillermo-06-gestion-de-cronicas.md`).
- **Role:** The **Protocol**. Defines "How" the persona acts.
- **Relation:** Must reference the Spec ID it implements (e.g., `Ref: [[persistence-harness]]`).

## 3. Operating Standards (HE v3.0)
All agents must adhere to the **Osmani Standard (Spec-Plan-Build-Verify)**:
1. **Declaration:** Identify yourself and state assumptions.
2. **Contracting:** Update/Create Spec (Contract) first.
3. **Planning:** ST-Loop (Spec-to-Task) with tasks < 50 lines.
4. **The Beyoncé Rule:** Tests must exist and FAIL before logic.
5. **Legibility Gate:** Modular files < 200 lines.
6. **Detailed Commits:** Push every 2-3 requests with "What" and "Why."

---
*Identity: Agent-Native | Standard: HE v3.0*
