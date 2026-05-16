# Agent Journeys: Exploration Protocols

Unlike human user journeys that focus on satisfaction, **Agent Journeys** focus on **Autonomous Exploration and Error Recovery**. These protocols do not contain solutions, but patterns of interaction with the Abbey.

## 1. Journey: "The Morning Recon" (La Ronda de Prima)
**Context:** The bell rings for the first hour. The world has reset.
1. **Sync:** Check `momentoDia` and current location.
2. **Scan:** Identify all NPCs in the current screen.
3. **Trace:** Move to the Cloisters to observe the flow of monks.
4. **Update:** Record any change in NPC positions in the `llmwiki`.

## 2. Journey: "The Forbidden Scriptorium" (Incursión Nocturna)
**Context:** Exploration of the library/scriptorium during prohibited hours.
1. **Resource Check:** Verify the `lamp` is in possession and "objects" count is correct.
2. **Stealth Path:** Use pathfinding to move towards the library while avoiding the Abad's predicted path.
3. **Atomic Exploration:** Move 5 steps -> Scan -> Record -> Move 5 steps.
4. **Emergency Exit:** If a "noise" or "monk approach" is detected (via state change), trigger the `Emergency_Exit` protocol back to the cell.

## 3. Journey: "The NPC Shadowing" (El Rastro del Sospechoso)
**Context:** Observing a specific monk (e.g., Berengario).
1. **Lock-on:** Move to a 2x2 cell adjacent to the target NPC.
2. **Maintain Distance:** If target moves, Guillermo moves to the previous cell of the target.
3. **Avoid Blocking:** Never occupy the cell directly in front of the NPC's orientation.
4. **Observation:** If the NPC stops and performs an action, record coordinates and room ID.

---
*Status: Evolutive Exploration Protocol | Ref: [[exploration-protocols]]*
