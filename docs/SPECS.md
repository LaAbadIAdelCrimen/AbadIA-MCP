# Project Specifications: AbadIA-MCP

## 1. System Overview
AbadIA-MCP is an AI-powered system designed to play "The Abbey of Crime". It consists of two main components:
- **MCP Server**: A FastAPI-based bridge that translates high-level AI commands into low-level game actions.
- **AI Agent**: A strategic thinker built with the Google Agent Developer Kit (ADK) that operates as "William of Baskerville".

## 2. Architecture
The system follows a strategic/driver split:
- **Strategic Layer (AI Agent)**: Decides *what* to do based on game goals and state.
- **Action Layer (MCP Server)**: Decides *how* to execute those actions (pathfinding, timing, etc.).

## 3. MCP Server API Specifications

### 3.1 High-Level Tools
These tools are exposed to the AI Agent for strategic interaction:
- `move_to_location(location: str)`: Navigates the character to a named location.
- `investigate_location(location: str)`: Performs investigation actions at a site.
- `talk_to_character(character: str)`: Initiates dialogue with NPCs.
- `get_full_game_state()`: Retrieves the complete JSON state from the emulator.
- `send_game_command(command: str)`: Sends low-level commands (UP, DOWN, LEFT, RIGHT, SPACE).

### 3.2 Movement & Orientation Logic
Movement depends on the character's orientation:
- **Orientations**: 0: E, 1: N, 2: W, 3: S.
- **Command Transformation**: To move in a cardinal direction, the agent must first face that direction.
- **path2Pos Mapping**:
    - `0N` (Facing East, Move North): `LEFT:UP:UP`
    - `1N` (Facing North, Move North): `UP:UP`
    - ... (and so on for all 32 combinations N, NE, E, SE, S, SW, W, NW).

### 3.3 Map Representation
The game world is represented as a 3D grid (Floor, X, Y):
- **Cell Structure**: `{"h": height, "c": character_id, "o": object_id, "r": room_id}`.
- **Compaction**: Cells with default values are stored as `null` to save space.

## 4. AI Agent Specifications

### 4.1 Persona: William of Baskerville
The agent follows the persona of the protagonist from "The Name of the Rose":
- Observant, analytical, and respectful of the Benedictine rules.
- **Rules of the Order**: Must comply with the abbey's schedule (Vespers, Mass, etc.) and stay with the novice Adso.

### 4.2 Decision Loop
1. **Analyze**: Fetch state via `get_full_game_state`.
2. **Plan**: Select a strategy via `planner.txt` based on `goals.md`.
3. **Execute**: Break down strategy into tool calls via `executor.txt`.

## 5. Data Models (Full Game State JSON)
The core data structure returned by the emulator:

```json
{
  "status": "OK",
  "data": {
    "Objetos": [],
    "Personajes": [
      {
        "altura": 0,
        "id": 0,
        "nombre": "Guillermo",
        "objetos": 32,
        "orientacion": 0,
        "posX": 136,
        "posY": 168
      }
    ],
    "Rejilla": [...],
    "bonus": 0,
    "dia": 1,
    "haFracasado": false,
    "investigacionCompleta": false,
    "momentoDia": 4,
    "numPantalla": 23,
    "obsequium": 31,
    "planta": 0
  }
}
```

## 6. Technologies
- **Backend**: Python 3.9+, FastAPI, Pydantic, Uvicorn.
- **AI**: Google Agent Developer Kit (ADK), Gemini Pro.
- **Interface**: MCP (Model Control Program) Server.