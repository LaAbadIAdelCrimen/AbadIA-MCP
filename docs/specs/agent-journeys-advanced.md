# Journey: "The Abbot's Shadow" (Seguir al Abad)

**Context:** The Abbot is in the same screen and issues a directive (e.g., "Sígueme" or "A la iglesia").
1. **Listen:** Identify the `frase_id` corresponding to a command.
2. **Track:** Identify the Abbot (`id: 4` or variable) in the characters array.
3. **Shadow Loop:**
   - Wait for the Abbot to move.
   - Maintain a distance of 2-3 cells.
   - Use pathfinding to the Abbot's previous position.
4. **Compliance Verification:** Monitor `obsequium`. If it increases or remains stable, the journey is succeeding.

---

# Journey: "The Library's Breath" (Sentir el Laberinto)

**Context:** Navigation inside the Planta 1 (Library) using sounds and air currents.
1. **Breadcrumb Loop:** Drop a mental marker every 5 cells.
2. **Listen for Danger:** If `sonido_id` indicates steps and no NPC is visible, stop and wait.
3. **Oil Management:** If Adso mentions the lamp, prioritize the exit journey immediately.
4. **Automatic Discovery:** Map every cell visited using the volume 2x2 logic.

---
*Status: Advanced Journeys | Ref: [[advanced-exploration]]*
