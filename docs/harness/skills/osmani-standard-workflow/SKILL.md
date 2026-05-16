---
name: osmani-standard-workflow
description: Implementation of the Osmani Standard for Agentic Engineering. Enforces the Spec-Plan-Build-Verify cycle to ensure production-grade output.
category: software-development
version: 1.0.0
---

# The Osmani Standard: Spec-Plan-Build-Verify

This skill defines the high-velocity, high-quality development cycle for AI agents. It acts as the "Process Harness" to prevent "Vibe Coding."

## The 4-Stage Cycle

### 1. SPEC (Specification)
- **Goal:** Define the "What" and the "How to Verify" before touching code.
- **Rule:** Every feature/fix must have a `SPEC.md` (or similar).
- **Content:** 
  - Context & Goal.
  - Acceptance Criteria.
  - **Verification & DoD:** Exact commands to run and expected outputs.
- **Agent Constraint:** If the spec is missing or ambiguous, stop and ask.

### 2. PLAN (Planning)
- **Goal:** Break the spec into atomic, executable tasks.
- **Protocol:** Implement the **Spec-to-Task (ST) Loop**.
- **Rule:** Tasks must be < 50 lines of change.
- **Agent Constraint:** No execution without a verified plan in the context.

### 3. BUILD (Construction)
- **Goal:** Implement the logic following the plan.
- **Rule:** Follow the **Beyoncé Rule** (Test-First).
- **Rule:** Maintain **Agent Legibility** (Files < 200 lines).

### 4. VERIFY (Verification)
- **Goal:** Prove the implementation works according to the Spec.
- **Action:** Run the commands defined in the "Verification & DoD" section of the Spec.
- **Evidence:** Capture and present the command output (logs, test results).

---
*Derived from the principles of Addy Osmani (2026).*
