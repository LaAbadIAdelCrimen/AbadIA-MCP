from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from ..mcp.server import mcp_server
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class Message(BaseModel):
    content: str
    type: Optional[str] = "text"

class MessageResponse(BaseModel):
    id: str
    status: str
    message: Message

class MCPMessage(BaseModel):
    type: str
    content: Dict
    target_clients: Optional[List[str]] = None

class MCPResponse(BaseModel):
    status: str
    message_id: str
    recipients: int

@router.post("/messages/", response_model=MessageResponse)
async def create_message(message: Message):
    """
    Create a new message
    """
    try:
        # Here you would typically process the message with MCP
        return MessageResponse(
            id="123",
            status="sent",
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    """
    Get a specific message by ID
    """
    # Here you would typically fetch the message from storage
    return MessageResponse(
        id=message_id,
        status="received",
        message=Message(content="Example message")
    )

@router.post("/send", response_model=MCPResponse)
async def send_mcp_message(message: MCPMessage):
    """
    Send a message through the MCP server
    """
    try:
        if message.target_clients:
            # Send to specific clients
            sent_count = 0
            for client_id in message.target_clients:
                if client_id in mcp_server.connections:
                    connection = mcp_server.connections[client_id]
                    await connection.send(json.dumps({
                        "type": message.type,
                        "content": message.content
                    }))
                    sent_count += 1
            
            return MCPResponse(
                status="sent",
                message_id=f"msg_{id(message)}",
                recipients=sent_count
            )
        else:
            # Broadcast to all clients
            await mcp_server.broadcast({
                "type": message.type,
                "content": message.content
            })
            
            return MCPResponse(
                status="broadcast",
                message_id=f"msg_{id(message)}",
                recipients=len(mcp_server.connections)
            )
    except Exception as e:
        logger.error(f"Error sending MCP message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clients")
async def get_connected_clients():
    """
    Get list of connected MCP clients
    """
    return {
        "total_clients": len(mcp_server.connections),
        "clients": [str(conn_id) for conn_id in mcp_server.connections.keys()]
    }

@router.post("/command")
async def send_command(command: Dict):
    """
    Send a command to all connected clients
    """
    try:
        await mcp_server.broadcast({
            "type": "COMMAND",
            "content": command
        })
        return {
            "status": "command_sent",
            "recipients": len(mcp_server.connections)
        }
    except Exception as e:
        logger.error(f"Error sending command: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 