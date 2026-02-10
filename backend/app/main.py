import logging
import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Startup logs for debugging
logger.info("=" * 60)
logger.info("🚀 STARTING 100HYPE FASTAPI APPLICATION")
logger.info(f"PORT from env: {os.getenv('PORT', 'NOT SET - using 8000')}")
logger.info(f"DATABASE_URL configured: {bool(settings.DATABASE_URL)}")
logger.info(f"BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")
logger.info(f"GOOGLE_CLIENT_ID configured: {bool(settings.GOOGLE_CLIENT_ID)}")
logger.info(f"GOOGLE_CLIENT_SECRET configured: {bool(settings.GOOGLE_CLIENT_SECRET)}")
logger.info(f"SECRET_KEY configured: {bool(settings.SECRET_KEY)}")
logger.info("=" * 60)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Configuração Dinâmica do CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # Converte as URLs para string (Pydantic retorna objetos URL)
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "100HYPE API is running 🚀"}