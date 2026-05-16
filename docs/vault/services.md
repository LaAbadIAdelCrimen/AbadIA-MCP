# Vault: Services & Infrastructure (Deep Technical)

Detailed connection contracts for the AbadIA environment.

## 1. Game Emulator (AbadIA-Server)
- **URL:** `http://localhost:4477`
- **Primary Endpoint:** `GET /abadIA/game/current`
- **Actions Endpoint:** `POST /abadIA/game/current/actions/{CMD}`
  - Valid CMDs: `UP`, `DOWN`, `LEFT`, `RIGHT`, `SPACE`.
- **Map Endpoint:** `GET /abadIA/game/map` (Returns the full 3D matrix).

## 2. MCP Bridge (AbadIA-MCP)
- **URL:** `http://localhost:8000`
- **Spec:** SSE (Server-Sent Events) via FastMCP.
- **Tools Schema:** Available at `GET /mcp/tools`.
- **SSE Stream:** `GET /mcp/sse`.

## 3. Knowledge Context
- **Wiki Root:** `~/abadIA-MCP/docs/wiki/`
- **Vault Root:** `~/abadIA-MCP/docs/vault/`
- **Log Sink:** `~/abadIA-MCP/storage/session_logs.jsonl`

---
*Ref: [[service-contracts-detailed]]*
