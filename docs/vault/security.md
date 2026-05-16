# Vault: Security & Compliance

Operational safety and game-rule compliance standards for the agent.

## 1. Monastic Compliance (Obsequium)
- **Threshold (Normal):** `> 15`. Safe for exploration.
- **Threshold (Warning):** `10 - 15`. Prioritize rule-following (Mass/Cell).
- **Threshold (Critical):** `< 10`. Mandatory return to cell or church. Immediate suspension of investigation.

## 2. Data Integrity
- **JSON Schema Validation:** All responses from `/abadIA/game/current` must be validated against the `data-models.md` spec to prevent "hallucination loops".
- **Path Verification:** No movement command is sent without 2x2 volume validation.

## 3. Failure States
- **Expulsion:** When Obsequium reaches 0.
- **Capture:** Detection by the Abbot in forbidden areas (Library at night).
- **Starvation:** Running out of "oil" for the lamp.

---
*Ref: [[monastic-compliance]]*
