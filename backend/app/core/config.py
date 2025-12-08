from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Invest-AI 2.0 API"
    API_V1_STR: str = "/api/v1"
    
    # Banco de Dados e IA
    DATABASE_URL: str
    GEMINI_API_KEY: str
    
    # Segurança
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # E-mail (Adicionado para corrigir o erro)
    EMAIL_SENDER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None
    EMAIL_RECEIVER: Optional[str] = None  # <--- Adicionado
    
    # Configurações Gerais
    LOG_LEVEL: str = "INFO"

    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        # Esta linha é a 'bala de prata': ignora variáveis extras no .env sem dar erro
        extra = "ignore"

settings = Settings()