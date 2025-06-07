from pydantic_settings import BaseSettings
from typing import Optional
import logging

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "AbadIA-MCP"
    DEBUG: bool = False
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # MCP Settings
    MCP_HOST: str = "0.0.0.0"  # Changed to 0.0.0.0 to accept external connections
    MCP_PORT: int = 5000
    MCP_MAX_CONNECTIONS: int = 100
    MCP_HEARTBEAT_INTERVAL: int = 30  # seconds
    MCP_CONNECTION_TIMEOUT: int = 60  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Security
    API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

    def setup_logging(self):
        """Configure logging based on settings"""
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ) 