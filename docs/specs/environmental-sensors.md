# Environmental Sensors & Experiential Logic

The AbadIA environment is not just a 3D grid; it is a multisensory world. Following HE v3.0, the agent must "feel" the environment through data arrays that represent sounds and visual messages.

## 1. Acoustic Sensors (Sonidos)
The game state returns a `sonidos` array. These correspond to acoustic signals (beeps, bells, steps).
- **Bell (Campana):** Indicates a change in the `momentoDia`. Triggers an immediate "Plan Re-evaluation".
- **NPC Steps:** Proximity of a monk outside the visual field. High risk in prohibited areas.

## 2. Narrative Sensors (Frases)
The `frases` array contains IDs of text messages displayed in the game.
- **The Abbot's Voice:** Commands like "Sígueme" (Follow me) or "A la iglesia" (To the church).
- **Adso's Warnings:** Context about the lamp ("Se apaga la lámpara") or the schedule.

## 3. Resource Sensors (Objetos)
Tracking the state of inventory as a survival constraint.
- **The Lamp:** If objects include `lámpara`, check for state changes in the environment (luminosity).

## 4. Verification & Validation (Detailed)

To verify the experiential sensor integration:

1. **Acoustic Trigger Test:**
   Manually trigger a bell in the game or use a mock state with a `sonido_id` corresponding to a bell.
   **Success Criteria:**
   - The agent's log must show a log entry with the label `[RE-EVALUATION] Reason: Bell signal detected`.
   - The goal stack must update based on the new `momentoDia`.

2. **Dialogue Reaction:**
   Wait for the Abbot to say "Sígueme" or "A la iglesia" (look for the specific `frase_id` in the game state).
   **Success Criteria:**
   - The agent must interrupt its current journey and switch to `guillermo-05-seguimiento-npc`.
   - The distance between Guillermo and the Abbot must remain < 5 cells.

3. **Sensor Log Audit:**
   Run the experiential auditor:
   ```bash
   python3 scripts/dreamer.py --analyze-sensory
   ```
   **Success Criteria:**
   - The report confirms that the delay between a sensor event (Sound/Phrase) and the corresponding agent action was < 3 command cycles.

---
*Status: Multisensory Harness | Ref: [[experiential-sensors]]*
