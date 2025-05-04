from pydantic import BaseModel
from typing import Optional

class MCPRequest(BaseModel):
    command: str
    parameters: Optional[dict] = None

class MCPResponse(BaseModel):
    status: str
    data: Optional[dict] = None
    error: Optional[str] = None 