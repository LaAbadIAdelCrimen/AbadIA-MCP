# Journey: guillermo-adso-05-el-centinela-y-tapon

**Context:** Restricting NPC movement in narrow corridors or stairs during prohibited activities.

## 1. Protocol
1. **Targeting:** Identify a "Bottleneck" (pasillo estrecho or escalera 2xN).
2. **Positioning:** Move Adso to the center of the bottleneck using standard following.
3. **Activation:** Guillermo uses `toggle_adso` (S key) to plant Adso.
4. **Investigation:** Guillermo performs prohibited actions (e.g., entering the scriptorium at night).
5. **Detection:** Monitor NPC positions. If an NPC (Abbot/Jorge) reaches Adso's volume, they are blocked.

## 2. Verification & Validation (Detailed)

To verify the Sentinel protocol:

1. **Bottleneck Blocking Test:**
   Run the collision simulation:
   ```bash
   python3 scripts/test_movement_logic.py --scenario bottleneck-block
   ```
   **Success Criteria:**
   - The simulation must show an NPC path calculation failing when Adso is parked in a 2-cell wide corridor.
   - The `check_volume_walkable` function must return `False` for the NPC trying to pass through Adso.

2. **In-Game Verification:**
   - Position Adso in the stairs to the Library.
   - Trigger `toggle_adso`.
   - Observe if the Abbot gets stuck in his routine path.
   **Success Criteria:**
   - The Abbot's coordinates remain static at the edge of Adso's 2x2 volume.
   - Guillermo's Obsequium does not decrease (as the Abbot cannot reach him).

3. **Cleanup:**
   - Call Adso back after the mission.
   - Verify the bottleneck is clear for NPCs.
