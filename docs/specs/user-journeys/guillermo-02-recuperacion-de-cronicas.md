# Agent Journey: guillermo-02-recuperacion-de-cronicas
Persona: Guillermo de Baskerville
Status: Proposed
Mode: Exploitation
Ref: [[persistence-harness]], [[ADR-010]]

## 1. Goal
Optimize token usage and time by resuming the investigation from a previously validated state (Checkpoint) instead of Guillermo's cell.

## 2. Heuristic Protocol

### Phase 1: Snapshot Discovery
1. **Action:** Query `persistence_harness` for available snapshots.
2. **Analysis:** Select the snapshot with the highest `obsequium` that is closest to the next investigation target (e.g., Library).

### Phase 2: Restoration
1. **Action:** Call `load_game_state(checkpoint_id)`.
2. **Verification:** Confirm `NumPantalla`, `posX`, `posY`, and `Planta` match the snapshot metadata.
3. **Integrity Check:** Verify `obsequium` is exactly as recorded.

### Phase 3: Resuming Exploration
1. **Handoff:** Transfer current state context to the [[guillermo-01-la-llamada-del-abad]] exploration loop (Phase 2).

## 3. Success Criteria
- [ ] Correct snapshot identified.
- [ ] Game state restored without Obsequium loss.
- [ ] Agent context window updated with the "jump" in time/position.

---
*Identity: Agent-Native | Standard: HE v3.0*
