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
