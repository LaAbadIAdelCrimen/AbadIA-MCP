# Journey: guillermo-04-incursion-nocturna

**Context:** Entry into the Library or Scriptorium during "Nocturnes".

## 1. Protocol
1. **Stealth Mode:** Prioritize movement to cells with maximum distance from the Abbot's predicted coordinates.
2. **Vision Check:** Verify `lámpara` in inventory.
3. **Scan Frequency:** execute `get_full_game_state` every 2 commands.
4. **Emergency Exit:** If a "step" sound is heard or Abbot is in field of view, retreat to the cell using the `breadcrumb buffer`.

## 2. Verification & DoD
- **Implemented if:** Guillermo enters the library at night and returns to his cell without being caught.
- **DoD:** At least 5 new library cells are mapped in the `llmwiki`.
