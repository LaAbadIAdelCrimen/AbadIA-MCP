import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

# URL of the FastMCP server (must match the one in server.py)
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

async def connect_and_get_tools():
    """
    Connects to the MCP server via Streamable HTTP and gets the list of tools.
    """
    print(f"🔗 Connecting to MCP server at: {MCP_SERVER_URL}")
    
    # 1. Define the connection parameters for Streamable HTTP
    connection_params = StreamableHTTPConnectionParams(
        url=MCP_SERVER_URL 
        # NOTE: In ADK, the 'StreamableHTTPConnectionParams' class encapsulates
        # the client logic for using this protocol.
    )

    # 2. Create an instance of MCPToolset (the ADK client)
    # MCPToolset handles the MCP handshake and fetching capabilities (tools).
    try:
        mcp_toolset = MCPToolset(
            connection_params=connection_params
        )
        await mcp_toolset.connect()
        exit_stack = await mcp_toolset.__aenter__()

        print("\n✅ Successful connection and Tools retrieved.")

        # 3. Access the list of available tools
        available_tools = mcp_toolset.get_tools()

        print("📋 List of Tools found:")
        if available_tools:
            for tool in available_tools:
                print(f"   - Name: {tool.name}")
                print(f"     Description: {tool.description}")
        else:
            print("   (No tools found)")
        
        # 4. It's important to clean up the toolset resources
        await exit_stack.aclose()

    except Exception as e:
        print(f"\n❌ Error connecting or retrieving tools: {e}")
        print("Make sure 'server.py' is running at the specified URL.")

if __name__ == "__main__":
    asyncio.run(connect_and_get_tools())
