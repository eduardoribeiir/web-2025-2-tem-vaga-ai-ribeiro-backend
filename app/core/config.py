from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./database.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 dias
    
    # API
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Tem Vaga Aí API"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
