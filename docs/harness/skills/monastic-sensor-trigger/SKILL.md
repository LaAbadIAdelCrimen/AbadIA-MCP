---
name: monastic-sensor-trigger
description: Automatic reaction engine for environmental signals (Sounds/Phrases). Deterministic plan re-evaluation without LLM inference.
category: software-development
version: 1.0.0
---

# Monastic Sensor Trigger (The Habit)

This skill monitors the multisensory arrays (`sonidos`, `frases`) and forces immediate state changes when specific monastic triggers are detected.

## 1. Capabilities
- **Bell Sync:** Detects `sonido_id` corresponding to bells and updates the local `current_horarium`.
- **Order Reaction:** Identifies command phrases (e.g., "Sígueme", "A misa") and sets the agent's `high_priority_mission`.
- **Interrupt Mode:** Can halt an active pathfinding script if a lethal threat is detected.

## 2. Usage
Inject the sensor monitor into the execution loop:
```bash
python3 scripts/sensor_trigger.py --status status.json
```

## 3. Strategic Why
Ensures 100% monastic compliance by treating religious duties as "Hard Interrupts" rather than "LLM Suggestions."

---
*Standard: [[experiential-harness-engineering]] | Part of Pack 012*
