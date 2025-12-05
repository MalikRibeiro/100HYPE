
from pydantic_settings import BaseSettings
from pydantic import ValidationError

class Settings(BaseSettings):
    PROJECT_NAME: str = "Invest-AI 2.0 API"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    GEMINI_API_KEY: str
    
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    EMAIL_SENDER: str | None = None
    EMAIL_PASSWORD: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
