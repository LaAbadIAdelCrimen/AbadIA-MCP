# Journey: guillermo-adso-04-el-hilo-de-ariadna

**Context:** Navigation in the Labyrinth or areas with identical screen layouts.

## 1. Protocol
1. **Detection:** Agent detects a "Visual Loop" (e.g., Room ID remains constant or transitions between screens result in identical height/furniture patterns).
2. **Deployment:** Guillermo uses the `toggle_adso` tool (S key) to leave Adso in the current room.
3. **Exploration:** Guillermo explores adjacent rooms.
4. **Reference:** Adso's position (available in `Personajes`) acts as the "Zero Point" or "Ariadne's Thread".
5. **Re-connection:** Once the exit or a unique landmark is found, Guillermo returns to Adso or calls him using `toggle_adso` again.

## 2. Verification & Validation (Detailed)

To verify the "Ariadne's Thread" protocol:

1. **Labyrinth Simulation:**
   Run the labyrinth navigation test:
   ```bash
   python3 scripts/test_pathfinding.py --area labyrinth --use-companion
   ```
   **Success Criteria:**
   - The agent must trigger `toggle_adso` after 3 identical screen detections.
   - The internal map must mark the cell with Adso as `MARKER_COMPANION`.

2. **State Verification:**
   Query the MCP state after deployment:
   ```bash
   curl -s http://localhost:8000/status | jq '.data.Personajes[] | select(.nombre=="Adso")'
   ```
   **Success Criteria:**
   - Adso's coordinates must remain static for at least 10 game ticks while Guillermo moves.

3. **Re-call Test:**
   - Verify that the agent sends the `S` command again when the investigation is complete.
   - Adso's coordinates must begin to change, maintaining distance `d < 5` from Guillermo.
