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
1. **The Interview Gateway:** Before creating a `SPEC.md` or `PLAN.md`, the agent MUST invoke the `interview-me` skill. Action is forbidden until user intent is extracted with 95% confidence.
2. **Declaration:** Identify yourself and state your assumptions before acting.
3. **Contracting:** Create/update `SPEC.md` or a Service-Level ADR in `docs/adr/`.
3. **The Beyoncé Rule:** Tests in `tests/` MUST exist and FAIL before logic is implemented.
4. **Agent Legibility Gate:** 
   - Files must be < 200 lines. 
   - Use modular, self-documenting code (Atoms/Molecules).
   - Refactor if complexity exceeds agentic context efficiency.

## 3. The Rule of Perfect Grace (Monastic Logic)
**Zero Obsequium Loss Goal:** It is possible to complete the game with 100% obsequium (Value: 31).

### Obsequium Runtime Modes (Max: 31):
1. **Exploration Mode:**
   - **Goal:** Discovery and Mapping.
   - **Behavior:** The agent is allowed to "sacrifice" Obsequium to access dangerous areas or test movement boundaries.
   - **Hard Limit:** 0 (Game Over). If `obsequium <= 27`, Adso must flag that a mistake was made, but mapping continues until 0. At 0, the agent MUST stop and perform a final `save_map`.
2. **Exploitation Mode:**
   - **Goal:** Solving/Perfect Run.
   - **Behavior:** ZERO tolerance for Obsequium loss.
   - **Hard Limit:** If `obsequium < 31`, the execution is aborted immediately to prevent a non-perfect state.

- If a hard limit is hit, the agent must use the **Persistence Harness** to rollback or report the failure to The Abbot.

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
