# AbadIA MCP Server: Technical Information

This document provides a detailed technical overview of how the AbadIA MCP Server operates, including its architecture, core logic, and API structure.

## 1. Architecture: FastAPI + MCP

The server is built using **FastAPI** as the primary web framework. It integrates the official **Model Context Protocol (MCP)** Python SDK via `FastMCP`.

- **FastAPI Foundation**: Provides the REST API endpoints, automatic Swagger documentation (`/docs`), and request handling.
- **MCP Layer (SSE)**: Exposes high-level tools via a dedicated **Server-Sent Events (SSE)** transport. The MCP application is mounted on `/mcp` and handles streaming communication.
- **Dual Support**: The server maintains full compatibility with legacy REST clients while offering a modern, real-time interface for AI agents.

## 2. Core Logic

### 2.1 Orientation-Based Movement (`path2Pos`)

Moving in the game is not as simple as sending cardinal directions. It depends on the character's (Guillermo) current orientation.

- **Orientations**:
  - `0`: East (E)
  - `1`: North (N)
  - `2`: West (W)
  - `3`: South (S)

- **Mapping**: The `path2Pos` dictionary in `server/main.py` maps a combination of `[orientation][direction]` to a sequence of low-level commands.
  - *Example*: If Guillermo is facing East (`0`) and wants to move North (`N`), the command sequence is `LEFT:UP:UP` (Turn left, then two steps forward).

### 2.2 Pathfinding (`A*`)

The server implements a standard **A* algorithm** to find paths between coordinates.
- **Grid Navigation**: The abbey is represented as a 3D grid (Floor, X, Y).
- **Navigability**: A cell is considered "walkable" if it is empty (`None`) or its height attribute (`h`) is below a certain threshold (typically 16).
- **Command Conversion**: Once a path of coordinates is found, it is converted into a sequence of `UP`, `DOWN`, `LEFT`, `RIGHT` commands.

### 2.3 Map Representation & Storage

The server maintains an in-memory representation of the game world.
- **Compact Format**: To save memory, empty cells (default height 0, no objects/characters) are stored as `None`.
- **Automatic Truncation**: During initialization, the map is truncated to specific dimensions (e.g., floor 0 is 256x256) to maintain performance.
- **Persistence**: Maps can be saved to and loaded from the `storage/` directory as JSON files.

## 3. API Endpoints

### System Endpoints
- `GET /status`: Retrieves current game status from the emulator.
- `GET /reset`: Resets the game to its starting point.
- `GET /game/cmd/{cmd}`: Sends a low-level command (UP, DOWN, LEFT, RIGHT, SPACE).
- `GET /game/move/{cmd}`: High-level cardinal movement (N, NE, E, SE, S, SW, W, NW).
- `GET /internal_status`: Returns the current internal game state (day, notes, discovered locations).

### Map Endpoints
- `GET /map/ascii`: Generates a real-time ASCII art representation of the current floor, optionally centered on Guillermo.
- `POST /map/save/{name}`: Persists the current map state to `storage/{name}.json`.
- `POST /map/load/{name}`: Loads a map from `storage/{name}.json` into memory.

### MCP Tools
- `move_to_location`: Higher-level navigation to named locations (e.g., 'library').
- `investigate_location`: Navigates to a spot and performs an action (SPACE).
- `talk_to_character`: Navigates to an NPC and initiates dialogue.
- `find_path_to_location`: Calculates path commands to reaching specific coordinates.

## 4. Initialization Workflow

1. **Startup**: `initialize_map()` is called.
2. **Persistence Check**: It looks for `storage/current_map.json`.
3. **Fallback**: If not found, it loads `storage/default_map.json`.
4. **Truncation**: The loaded map is truncated to optimize memory usage.
