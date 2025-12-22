import asyncio
from mcp.server.fastmcp import FastMCP
m = FastMCP("test")
@m.tool()
async def foo(a: int):
    """Test tool"""
    return a

async def main():
    tools = await m.list_tools()
    import json
    # Tools are Tool objects, we want to see their dict representation
    print([{"name": t.name, "description": t.description, "inputSchema": t.inputSchema} for t in tools])

asyncio.run(main())
