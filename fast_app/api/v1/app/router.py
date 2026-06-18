from fastapi import APIRouter
from fast_app.api.v1.app.routes import health
from fast_app.api.v1.app.routes import wa_webhook

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(wa_webhook.router, tags=["WhatsApp webhook"])
