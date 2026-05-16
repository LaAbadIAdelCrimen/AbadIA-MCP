# Concept: The Osmani Standard (Process Harness)

In the context of **AbadIA**, the Osmani Standard is the "Rule of Saint Benedict" for development. It ensures that any agent (Hermes, Claude, or a subagent in Antigravity) follows a predictable and high-quality path.

## 1. The Cycle: Spec-Plan-Build-Verify

Following the advice of **Addy Osmani**, we treat the development process as a series of gates:

1.  **Gate 1 (Spec):** No code is written without a contract. Every Journey and Persona in `docs/specs/` is a contract.
2.  **Gate 2 (Plan):** Every Spec is converted into an atomic Task list. No "freestyle" coding.
3.  **Gate 3 (Build):** Implementation must respect the **200-line Rule** (Agent Legibility).
4.  **Gate 4 (Verify):** Success is not "it feels okay," but "the test passed with this output."

## 2. Autonomous Sovereignty

The goal is for **AbadIA** to be self-healing and self-documenting. 
- When an agent encounters an error, it doesn't just fix it; it updates the **Vault** or creates a new **ADR** to prevent the error in the future.
- This is the **"Process Harness"**.

---
*Ref: [[osmani-standard-workflow]], [[harness-standard-v3]]*
