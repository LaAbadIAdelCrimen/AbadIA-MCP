---
name: abadia-logic-validator
description: Local logic validator to offload geometry and collision checks from the LLM. High-efficiency deterministic validation.
category: software-development
version: 1.0.0
---

# AbadIA Logic Validator (High-Efficiency)

This skill offloads spatial reasoning and collision detection from the LLM to local scripts. Use this before proposing a movement to ensure it adheres to the 2x2 monastic volume rule.

## 1. Capabilities
- **Volume Check:** Validates if a 2x2 entity fits in a target coordinate.
- **Clearance Audit:** Checks for NPCs or static objects in the immediate trajectory.
- **Height delta:** Ensures `abs(h_target - h_current) <= 2`.

## 2. Usage
Trigger the local validator script:
```bash
python3 scripts/logic_validator.py --x <dest_x> --y <dest_y> --floor <floor>
```

## 3. strategic Why
Reduces token consumption and latency by replacing LLM-based spatial estimation with deterministic geometric calculations.

---
*Standard: [[harness-standard-v3]] | Part of Pack 012*
