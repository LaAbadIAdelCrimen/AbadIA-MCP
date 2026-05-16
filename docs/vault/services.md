# Vault: Services & Infrastructure

This document defines the connection contracts for all external and internal services required by the AbadIA Agent.

## 1. Game Emulator (AbadIA-Server)
- **Primary Endpoint:** `http://localhost:4477`
- **Protocol:** REST / JSON
- **Health Check:** `GET /abadIA/game/current`
- **Responsibilities:** Emulates the original 1987 game logic and 3D grid.

## 2. MCP Bridge (AbadIA-MCP)
- **Primary Endpoint:** `http://localhost:8000`
- **Protocol:** MCP (Model Control Program) over SSE
- **Mount Point:** `/mcp`
- **Responsibilities:** Translates high-level agent tools into emulator actions.

## 3. Storage & Persistence
- **Map Data:** `~/abadIA-MCP/game_data/map.json`
- **State Logs:** `~/abadIA-MCP/storage/`
- **Format:** Standard JSON (case-sensitive characters/personajes).

---
*Ref: [[service-contracts]]*
