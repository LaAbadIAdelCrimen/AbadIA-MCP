# Vault: Security & Monastic Policies

Enforcing the "Safe Investigation" boundaries for the agent.

## 1. Monastic Safety (The Obsequium Harness)
The agent is restricted by the abbey's rules.
- **Rule A (Schedule):** No movement outside the cell during "Nocturnes" unless a `Forbidden_Exploration` protocol is active.
- **Rule B (Adso):** Never move more than 5 cells away from Adso (`id: 1` in characters).
- **Rule C (Abbot):** If the Abbot is in the same `numPantalla`, movement must be restricted to "Standard Compliance" (heading towards the church or refectory).

## 2. Technical Security
- **Command Gating:** `send_game_command` is rate-limited to 1 command per 200ms to prevent emulator desync.
- **Data Gating:** Any state where `haFracasado: true` must trigger an immediate `Monastic_Dreamer` session to analyze the death-cause and update the Vault.
- **Path Validation:** All `move_to` actions must be pre-validated by the `check_volume_walkable` logic in the Action Layer.

---
*Ref: [[monastic-security-policies]]*
