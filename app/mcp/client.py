from fastmcp import MCPClient
from ..config import Settings

settings = Settings()

class MCPClientHandler:
    def __init__(self):
        self.client = MCPClient(
            host=settings.MCP_HOST,
            port=settings.MCP_PORT
        )
    
    async def connect(self):
        """Connect to MCP server"""
        await self.client.connect()
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        await self.client.disconnect()
    
    async def send_message(self, message: str):
        """Send message to MCP server"""
        await self.client.send(message)
    
    async def receive_message(self):
        """Receive message from MCP server"""
        return await self.client.receive() 