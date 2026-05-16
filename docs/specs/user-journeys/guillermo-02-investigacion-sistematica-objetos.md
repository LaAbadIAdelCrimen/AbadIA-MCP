# Journey: guillermo-02-investigacion-sistematica-objetos

**Context:** Entry into a room or detected change in `objetos`.

## 1. Protocol
1. **Detection:** Read the `objetos` array from game state.
2. **Prioritization:** Sort objects by proximity to Guillermo.
3. **Iteration:**
   - Move to a cell adyacent to Object ID.
   - Send `SPACE` / `investigate_location`.
   - Capture the response and log it as "Discovered Evidence".
4. **Persistence:** Update the `llmwiki` entry for the current room with object details.

## 2. Verification & DoD
- **Implemented if:** The agent successfully logs a new object description after discovery.
- **DoD:** All objects present in the JSON state are documented in the wiki.
