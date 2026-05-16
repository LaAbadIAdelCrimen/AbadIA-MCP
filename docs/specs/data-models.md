# Data Models and Game State

## 1. Game State JSON Structure
The core state returned by the emulator/server.

```json
{
  "status": "OK",
  "data": {
    "personajes": [
      {
        "id": 0,
        "nombre": "Guillermo",
        "posX": 136,
        "posY": 168,
        "orientacion": 0,
        "altura": 0,
        "objetos": 0
      }
    ],
    "objetos": [],
    "rejilla": [[...]],
    "dia": 1,
    "momentoDia": 4,
    "obsequium": 31,
    "planta": 0,
    "numPantalla": 23
  }
}
```

## 2. Key Definitions
- **obsequium:** The "life" bar. Decreases on rule violations.
- **momentoDia:** Integer `1-8` representing the monastic hours (Nocturnes to Compline).
- **rejilla:** 3D grid representation of the immediate surroundings.
- **planta:** Floor level (0: Ground, 1: Upper floors/Library).
- **numPantalla:** Unique ID of the current game screen.

## 3. Verification & Validation (Detailed)

To ensure the data model integrity, perform the following checks:

1. **Schema Compliance:**
   Fetch the game state and validate against the internal schema:
   ```bash
   curl -s http://localhost:8000/status | jq .
   ```
   **Success Criteria:**
   - The response must contain the top-level keys: `status` and `data`.
   - The `data` object must contain `Personajes`, `Planta`, `Rejilla`, and `NumPantalla`.

2. **Semantic Integrity:**
   - **Obsequium:** Manually trigger a rule violation in the game (e.g., skip a service) and verify that the `obsequium` value decreases in the JSON response.
   - **MomentoDia:** Wait for a bell and verify that the `momentoDia` value increments.
   - **Planta:** Move between floors and verify that the `planta` value changes correctly.

3. **Rejilla (Grid) Verification:**
   Run the map update test:
   ```bash
   python3 scripts/test_map_update.py
   ```
   **Success Criteria:**
   - The output must confirm that 'G' (Guillermo), 'a' (Adso), and objects are positioned correctly within the grid boundaries.
