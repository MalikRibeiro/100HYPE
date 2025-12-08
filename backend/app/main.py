
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router

from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Invest-AI 2.0 API"}
