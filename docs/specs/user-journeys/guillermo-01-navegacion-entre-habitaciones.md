# Journey: guillermo-01-navegacion-entre-habitaciones

**Context:** Move from current location to Room N (by ID or name).

## 1. Protocol
1. **Targeting:** Fetch target coordinates from `vault/services.md` or `llmwiki`.
2. **Initial Path:** Generate A* path based on static map.
3. **Execution Loop:**
   - Check `Personajes` array in every tick.
   - If a cell in the 2x2 volume path is occupied: Send `NOP`.
   - If blocked for > 2 ticks: Trigger Recalculation journey.
4. **Volume Validation:** Verify `abs(h_target - h_current) <= 2`.

## 2. Verification & DoD
- **Implemented if:** `tests/test_dynamic_navigation.py` passes with a moving NPC blocking the path.
- **DoD:** Guillermo reaches Room N without Obsequium penalty.
