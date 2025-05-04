from fastapi import APIRouter, HTTPException
from app.models.models import MCPRequest, MCPResponse
from app.services.mcp_client import MCPClient

router = APIRouter()

@router.post("/command", response_model=MCPResponse)
async def execute_command(request: MCPRequest):
    try:
        client = MCPClient()
        result = await client.execute_command(request.command, request.parameters)
        return MCPResponse(status="success", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 