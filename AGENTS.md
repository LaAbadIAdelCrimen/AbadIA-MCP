     1|# AGENTS.md — abadIA Autonomous Operations Manual (HE v3.0)
     2|
     3|This is the canonical source of truth for all autonomous agents (Gemini-cli, Antigravity/Honcho, Claude Code, Hermes) operating on the abadIA project.
     4|
     5|## 1. The Karpathy Standard
     6|**Harness Over Prompt:** We follow Karpathy's Law: Optimizing the evaluation arnés and deterministic environment is more critical than optimizing individual prompts. An agent's capability is capped by the quality of its harness.
     7|
     8|## 2. The Rule of Perfect Grace
     9|**Zero Obsequium Loss Goal:** It is possible to complete the game with 100% obsequium. 
    10|- If `obsequium` decreases, a plan has failed retrospective validation.
    11|- Agents must use the **Persistence Harness** to save state before risky actions and rollback on failure.
    12|
    13|## 2. Naming Conventions & Relationships
    14|To ensure HE validation, all documentation must follow this schema:
    15|
    16|### A. Specifications (`docs/specs/*.md`)
    17|- **Name:** `[system-component].md` (e.g., `movement.md`, `persistence-harness.md`).
    18|- **Role:** The **Contract**. Defines the "What" and "Validation Proofs."
    19|- **Relation:** Must list the User Journeys that implement it.
    20|
    21|### B. User Journeys (`docs/specs/user-journeys/*.md`)
    22|- **Name:** `[persona]-[id]-[action].md` (e.g., `guillermo-06-gestion-de-cronicas.md`).
    23|- **Role:** The **Protocol**. Defines "How" the persona acts.
    24|- **Relation:** Must reference the Spec ID it implements (e.g., `Ref: [[persistence-harness]]`).
    25|
    26|## 3. Operating Standards (HE v3.0)
    27|All agents must adhere to the **Osmani Standard (Spec-Plan-Build-Verify)**:
    28|1. **Declaration:** Identify yourself and state assumptions.
    29|2. **Contracting:** Update/Create Spec (Contract) first.
    30|3. **Planning:** ST-Loop (Spec-to-Task) with tasks < 50 lines.
    31|4. **The Beyoncé Rule:** Tests must exist and FAIL before logic.
    32|5. **Legibility Gate:** Modular files < 200 lines.
    33|6. **Detailed Commits:** Push every 2-3 requests with "What" and "Why."
    34|
    35|---
    36|*Identity: Agent-Native | Standard: HE v3.0*
    37|
## The Karpathy Standard (Software 3.0)
All agent operations follow the 4 Golden Rules:
1. **Strategic Thinking** (Plan before Build)
2. **Aggressive Simplicity** (Minimalist Code)
3. **Surgical Precision** (Scope Control)
4. **Verifiable Completion** (The Beyoncé Rule: "If you liked it, you should have put a test on it")
