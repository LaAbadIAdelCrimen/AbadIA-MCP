# Agent Journey: guillermo-01-la-llamada-del-abad
Persona: Guillermo de Baskerville
Status: Active
Mode: Exploration
Ref: [[navigation-map]], [[mcp-api]]

## 1. Goal
Initialize the monastic experience and establish the first contact with the Abbot to understand the investigation's constraints.

## 2. Heuristic Protocol

### Phase 1: Initialization (The Reset)
1. **Action:** Call `reset_game`.
2. **Verification:** Confirm `NumPantalla` is the initial room (usually Guillermo's cell or the entrance).
3. **Success Criteria:** `obsequium == 31`, `posX` and `posY` are valid.

### Phase 2: Heuristic Exploration
While `Abbot` is not in the same room (`numPantalla`):
1. **Sensory Check:** Inspect `Personajes` list in current game state.
2. **Decision Engine:**
   - If a new door/exit is visible in the ASCII map, move towards it using `find_path` or `get_possible_moves`.
   - If blocked, backtrack to the previous room.
   - **Constraint:** Maintain `obsequium > 27`. If it drops to 27, flag as "Protocol Deviation" but continue exploration until 0.

### Phase 3: The Interaction
If `Abbot` (ID 1) is detected:
1. **Action:** Navigate to the Abbot's coordinates using `find_path`.
2. **Action:** Execute `talk_to_character("abbot")` (Space command).
3. **Listening Hook:** Capture the response text from the Abbot.
4. **Capa 8 Integration:** Send the Abbot's words to the [[dreamer]] log for semantic synthesis.

## 3. Completion Criteria
- [ ] Game reset successfully.
- [ ] At least 3 rooms explored.
- [ ] Abbot's message captured and logged.

---
*Identity: Agent-Native | Standard: HE v3.0*
