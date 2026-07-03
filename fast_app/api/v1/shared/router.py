from fastapi import APIRouter

from fast_app.api.v1.shared.routes import auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"])
