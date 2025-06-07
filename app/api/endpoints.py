from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

class Message(BaseModel):
    content: str
    type: Optional[str] = "text"

class MessageResponse(BaseModel):
    id: str
    status: str
    message: Message

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