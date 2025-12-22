# Refactor Proposal: SSE MCP with official SDK and FastAPI

This proposal outlines the transition from the current `fastapi_mcp` integration to the official Anthropic `mcp` Python SDK using `FastMCP`. This will enable **SSE (Server-Sent Events)** support while maintaining the existing FastAPI functionality.

## Objectives
- **SSE Support**: Enable real-time, streaming communication for the MCP protocol.
- **Official SDK**: Switch to the industry-standard `mcp` python library for better long-term support.
- **Dual Mode**: Maintain the existing REST endpoints for legacy compatibility and internal tooling.

## Proposed Architecture: FastMCP + FastAPI Integration

The refactor will use the `FastMCP` class, which is designed to be easily embedded within FastAPI.

### 1. Unified Server Entry Point
We will initialize both `FastAPI` and `FastMCP`. The MCP server will be "mounted" onto the FastAPI application.

```python
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI(title="AbadIA Dual Server")
mcp = FastMCP("AbadIA", dependencies=["httpx", "requests"])

# Existing FastAPI endpoints remain untouched
@app.get("/status")
async def get_status():
    ...

# Define MCP tools using decorators
@mcp.tool()
async def move_to_location(location: str) -> str:
    """Moves Guillermo to a named location."""
    # Logic here
    return f"Moved to {location}"

# Integration: The magic happens here
# FastMCP handles the SSE and Tool calling logic automatically
```

### 2. SSE Transport Deployment
Instead of standard HTTP for tools, we will use the `StreamingResponse` from FastAPI or the built-in SSE transport provided by the SDK.

### 3. Key Changes

| Component           | Current State                        | Proposed State                                    |
| :------------------ | :----------------------------------- | :------------------------------------------------ |
| **MCP SDK**         | `fastapi_mcp` (custom)               | `mcp` (official) + `FastMCP`                      |
| **Transport**       | Standard HTTP                        | SSE (Server-Sent Events)                          |
| **Tool Definition** | Mix of regular routes and decorators | `@mcp.tool()` decorators                          |
| **Dependencies**    | Mixed                                | Clear separation of game logic vs transport logic |

## Implementation Steps

1. **Install Dependencies**: `pip install mcp[cli]`.
2. **Refactor Tool Definitions**: Move logic from current endpoints into dedicated `@mcp.tool()` functions.
3. **Internal Logic Extraction**: Move shared logic (game state, movement math) into a library-like structure to be used by both REST and MCP layers.
4. **SSE Mount**: Implement the mount point for the MCP SSE transport.

## Benefits
- **Concurrency**: SSE allows for a more responsive agent interaction.
- **Portability**: The server will work perfectly with standard MCP clients (Gemini, Claude, Cursor) through the SSE transport.
- **Cleanliness**: Decouples the "Game Control" logic from the "API Transport" logic.

> [!IMPORTANT]
> This refactor *will not* break existing tools. The REST endpoints will still function as a "backup" or for manual testing via `curl`.
