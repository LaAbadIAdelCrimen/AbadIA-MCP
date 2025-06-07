from fastmcp import MCPServer, MCPConnection
from typing import Dict, Optional
from ..config import Settings
import logging
import json

settings = Settings()
logger = logging.getLogger(__name__)

class AbadIAMCPServer:
    def __init__(self):
        self.server = MCPServer(
            host=settings.MCP_HOST,
            port=settings.MCP_PORT
        )
        self.connections: Dict[str, MCPConnection] = {}

    async def start(self):
        """Start the MCP server"""
        logger.info(f"Starting MCP server on {settings.MCP_HOST}:{settings.MCP_PORT}")
        await self.server.start()

    async def stop(self):
        """Stop the MCP server"""
        logger.info("Stopping MCP server")
        await self.server.stop()

    async def handle_connection(self, connection: MCPConnection):
        """Handle new MCP connection"""
        client_id = str(connection.id)
        logger.info(f"New connection from client {client_id}")
        self.connections[client_id] = connection

        try:
            while True:
                message = await connection.receive()
                if message:
                    await self.handle_message(connection, message)
        except Exception as e:
            logger.error(f"Error handling connection {client_id}: {str(e)}")
        finally:
            await self.handle_disconnect(connection)

    async def handle_message(self, connection: MCPConnection, message: str):
        """Handle incoming MCP message"""
        try:
            data = json.loads(message)
            message_type = data.get('type', 'unknown')
            content = data.get('content', {})

            logger.info(f"Received message type {message_type} from {connection.id}")

            # Handle different message types
            if message_type == "HELLO":
                await self.handle_hello(connection, content)
            elif message_type == "COMMAND":
                await self.handle_command(connection, content)
            elif message_type == "STATUS":
                await self.handle_status(connection, content)
            else:
                await connection.send(json.dumps({
                    "type": "ERROR",
                    "content": f"Unknown message type: {message_type}"
                }))

        except json.JSONDecodeError:
            await connection.send(json.dumps({
                "type": "ERROR",
                "content": "Invalid JSON format"
            }))
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await connection.send(json.dumps({
                "type": "ERROR",
                "content": "Internal server error"
            }))

    async def handle_hello(self, connection: MCPConnection, content: dict):
        """Handle HELLO message type"""
        await connection.send(json.dumps({
            "type": "WELCOME",
            "content": {
                "server": "AbadIA-MCP",
                "version": "1.0"
            }
        }))

    async def handle_command(self, connection: MCPConnection, content: dict):
        """Handle COMMAND message type"""
        command = content.get('command')
        if command:
            await connection.send(json.dumps({
                "type": "COMMAND_RESPONSE",
                "content": {
                    "status": "received",
                    "command": command
                }
            }))

    async def handle_status(self, connection: MCPConnection, content: dict):
        """Handle STATUS message type"""
        await connection.send(json.dumps({
            "type": "STATUS_RESPONSE",
            "content": {
                "server_status": "operational",
                "connected_clients": len(self.connections)
            }
        }))

    async def handle_disconnect(self, connection: MCPConnection):
        """Handle client disconnection"""
        client_id = str(connection.id)
        if client_id in self.connections:
            del self.connections[client_id]
            logger.info(f"Client {client_id} disconnected")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.connections.values():
            try:
                await connection.send(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting to {connection.id}: {str(e)}")

# Create singleton instance
mcp_server = AbadIAMCPServer() 