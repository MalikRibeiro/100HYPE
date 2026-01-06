
from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.endpoints import auth, portfolio, analysis

# api_router.include_router(auth.router, tags=["login"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
