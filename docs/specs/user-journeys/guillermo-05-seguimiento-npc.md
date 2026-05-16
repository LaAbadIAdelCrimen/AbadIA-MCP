# Journey: guillermo-05-seguimiento-npc

**Context:** Identification of a suspect NPC (e.g., Berengario) moving with intent.

## 1. Protocol
1. **Lock-on:** Move to a cell adjacent (but not blocking) the target.
2. **Shadow Pattern:** Follow the NPC's previous coordinates using A*.
3. **Volume Safety:** Maintain at least 1 cell of buffer to avoid collision with the target's 2x2 volume.
4. **Endpoint Recording:** If the target stops in a room and triggers an animation or state change, record coordinates.

## 2. Verification & DoD
- **Implemented if:** Guillermo follows an NPC for more than 2 screens without collision.
- **DoD:** The NPC's destination is logged in the session experience report.
