from fastapi import APIRouter
from fast_app.api.v1.app.routes import health
from fast_app.api.v1.app.routes import meta_webhook
from fast_app.api.v1.app.routes import conversation
from fast_app.api.v1.app.routes import channel_account
from fast_app.api.v1.app.routes import contact

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(meta_webhook.router, tags=["Meta webhook"])
api_router.include_router(conversation.router, tags=["Conversation"])
api_router.include_router(channel_account.router, tags=["Channel Account"])
api_router.include_router(contact.router, tags=["Contact"])
