from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "AbadIA-MCP"
    DEBUG: bool = False
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # MCP Settings
    MCP_HOST: str = "localhost"
    MCP_PORT: int = 5000
    
    # Optional API Key for security (if needed)
    API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env" 