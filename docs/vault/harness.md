# Vault: Harness Engineering Policies

The engineering lifecycle rules for the abadIA project.

## 1. The Beyoncé Rule
- **Standard:** "If you liked it, you should have put a test on it."
- **Policy:** No logic is implemented without a corresponding failing test in `tests/`.

## 2. Agent Legibility Gate
- **Standard:** Files must be strictly under 200 lines.
- **Policy:** If a file exceeds 150 lines, it must be audited for refactoring into a modular "Index-Pointer" pattern.

## 3. HE v3.0 Steps
1. **Anti-rationalization** (Question the current state).
2. **Spec** (Contracting).
3. **Plan** (Atomicity).
4. **Harness** (Testing).
5. **Build** (Modular implementation).
6. **Test** (Verification).
7. **Distill** (Skillify).

---
*Ref: [[harness-policies]]*
