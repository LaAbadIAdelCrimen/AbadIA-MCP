from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MCP Project"
    
    # MCP Settings
    MCP_HOST: str = "localhost"
    MCP_PORT: int = 9000
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 