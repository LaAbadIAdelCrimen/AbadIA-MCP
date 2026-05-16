# MCP API Specification

## 1. High-Level Tools
These tools are exposed to the AI Agent for strategic interaction via the MCP protocol.

| Tool Name | Parameters | Description |
|-----------|------------|-------------|
| `move_to_location` | `location: str` | Navigates the character to a named location (e.g., 'library'). |
| `investigate_location` | `location: str` | Performs investigation actions at a specific site. |
| `talk_to_character` | `character: str` | Initiates dialogue with NPCs. |
| `get_full_game_state` | None | Retrieves the complete JSON state from the emulator. |
| `send_game_command` | `command: str` | Sends low-level commands (UP, DOWN, LEFT, RIGHT, SPACE). |
| `find_path` | `x, y, floor` | Calculates a path of commands to specific coordinates. |
| `get_possible_moves` | None | Calculates walkable directions from the current position. |

## 2. Endpoints (Legacy REST)
- `GET /status`: Alias for full game state.
- `GET /game/cmd/{cmd}`: Direct command execution.
- `GET /map/ascii`: Returns a text-based visualization of the surrounding map.
- `POST /map/save/{name}`: Persists current map discovery to disk.

## 3. Communication Protocol
The server uses **FastAPI** with **FastMCP** for SSE (Server-Sent Events) support.
- **Default Port:** 8000
- **MCP Mount Point:** `/mcp`

## 4. Verification & Validation (Detailed)

Implementation is **Done** when:

1. **Tool Discovery:**
   Verify that the MCP server exposes all required tools:
   ```bash
   curl -s http://localhost:8000/mcp/tools | jq .
   ```
   **Success Criteria:**
   - The JSON output must list `move_to_location`, `investigate_location`, `talk_to_character`, `get_full_game_state`, `send_game_command`, `find_path`, `get_possible_moves`, and `toggle_adso`.

2. **Connectivity & Roundtrip:**
   Run the connection diagnostic:
   ```bash
   python3 scripts/check_connection.py
   ```
   **Success Criteria:**
   - 100% success rate for all endpoints.
   - Latency for the roundtrip must be < 500ms.

3. **Tool Functionality:**
   Test a high-level tool via the REST fallback:
   ```bash
   curl -s -X POST "http://localhost:8000/tools/move_to_location?location=library"
   ```
   **Success Criteria:**
   - The response message must indicate success.
   - The game state (`GET /status`) must reflect that commands were sent.
