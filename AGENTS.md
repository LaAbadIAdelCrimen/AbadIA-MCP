# AGENTS.md — abadIA Autonomous Operations Manual (HE v3.0)

This is the canonical source of truth for all autonomous agents (Gemini-cli, Antigravity/Honcho, Claude Code, Hermes) operating on the abadIA project.

## 1. The Karpathy Standard (Software 3.0)
**Harness Over Prompt:** We follow Karpathy's Law: Optimizing the evaluation arnés and deterministic environment is more critical than optimizing individual prompts. An agent's capability is capped by the quality of its harness.
1. **Strategic Thinking** (Plan before Build)
2. **Aggressive Simplicity** (Minimalist Code)
3. **Surgical Precision** (Scope Control)
4. **Verifiable Completion** (The Beyoncé Rule: "If you liked it, you should have put a test on it")

## 2. Operating Standards (HE v3.0)
All agents must adhere to the **Osmani Standard (Spec-Plan-Build-Verify)** and the 7-step deterministic cycle:
1. **Declaration:** Identify yourself and state your assumptions before acting.
2. **Contracting:** Create/update `SPEC.md` or a Service-Level ADR in `docs/adr/`.
3. **The Beyoncé Rule:** Tests in `tests/` MUST exist and FAIL before logic is implemented.
4. **Agent Legibility Gate:** 
   - Files must be < 200 lines. 
   - Use modular, self-documenting code (Atoms/Molecules).
   - Refactor if complexity exceeds agentic context efficiency.

## 3. The Rule of Perfect Grace (Monastic Logic)
**Zero Obsequium Loss Goal:** It is possible to complete the game with 100% obsequium. 
- If `obsequium` decreases, a plan has failed retrospective validation.
- Agents must use the **Persistence Harness** to save state before risky actions and rollback on failure.

## 4. Naming Conventions & Relationships
To ensure HE validation, all documentation must follow this schema:

### A. Specifications (`docs/specs/*.md`)
- **Name:** `[system-component].md` (e.g., `movement.md`, `persistence-harness.md`).
- **Role:** The **Contract**. Defines the "What" and "Validation Proofs."

### B. User Journeys (`docs/specs/user-journeys/*.md`)
- **Name:** `[persona]-[id]-[action].md` (e.g., `guillermo-06-gestion-de-cronicas.md`).
- **Role:** The **Protocol**. Defines "How" the persona acts.
- **Relation:** Must reference the Spec ID it implements (e.g., `Ref: [[persistence-harness]]`).

## 5. Toolchain & Interaction
- **Primary Interface:** `gemini-cli` + `antigravity`.
- **Memory:** `antigravity` (Honcho) captures the "Dreamer" state.
- **Skills:** This repository contains local skills in `.hermes/skills/`. Agents MUST load these skills (e.g., using `skill_view`) to handle project-specific workflows like `skillify`.

## 6. Atomic Teaching Protocol
No task is "Done" until the educational artifacts are generated:
- **Log:** Update `docs/wiki/log.md`.
- **Teaching:** New concept in `docs/wiki/concepts/`.
- **Production:** New pack in `docs/production/`.

---
*Identity: Agent-Native | Standard: HE v3.0*
