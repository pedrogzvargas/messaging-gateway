from fastapi import APIRouter
from fast_app.api.v1.app.routes import health
from fast_app.api.v1.app.routes import meta_webhook
from fast_app.api.v1.app.routes import conversation
from fast_app.api.v1.app.routes import channel_account
from fast_app.api.v1.app.routes import contact
from fast_app.api.v1.app.routes import message
from fast_app.api.v1.app.routes import faq
from fast_app.api.v1.app.routes import business_prompt
from fast_app.api.v1.app.routes import me
from fast_app.api.v1.app.routes import dashboard
from fast_app.api.v1.app.routes import ticket
from fast_app.api.v1.app.routes import notification_subscription
from fast_app.api.v1.app.routes import customer_notification

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(meta_webhook.router, tags=["Meta webhook"])
api_router.include_router(conversation.router, tags=["Conversation"])
api_router.include_router(channel_account.router, tags=["Channel Account"])
api_router.include_router(contact.router, tags=["Contact"])
api_router.include_router(message.router, tags=["Message"])
api_router.include_router(faq.router, tags=["Faq"])
api_router.include_router(business_prompt.router, tags=["Business Prompt"])
api_router.include_router(me.router, tags=["Me"])
api_router.include_router(dashboard.router, tags=["Dashboard"])
api_router.include_router(ticket.router, tags=["Ticket"])
api_router.include_router(notification_subscription.router, tags=["Notification Subscription"])
api_router.include_router(customer_notification.router, tags=["Customer Notification"])
