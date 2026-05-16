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

## 4. Verification & DoD
- **Sound Mapping:** A dictionary mapping `sonido_id` to its meaning exists and is verified by the Dreamer.
- **Dialogue Reaction:** Agent demonstrates a reaction to a specific `frase_id` (e.g., stopping movement when told "¡Guillermo!").
- **Audit:** Post-session logs show that no more than 2 command cycles passed between an acoustic signal and the agent's acknowledgment.

---
*Status: Multisensory Harness | Ref: [[experiential-sensors]]*
