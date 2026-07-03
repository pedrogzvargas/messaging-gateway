from fastapi import APIRouter
from fast_app.api.v1.app.routes import health
from fast_app.api.v1.app.routes import meta_webhook

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(meta_webhook.router, tags=["Meta webhook"])
