from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.whatsapp_webhook.domain import WhatsappWebhookRepository
from sqlalchemy_models import WhatsappWebhookModel
from .webhook_mapper import WebhookMapper


class PgWhatsappWebhookRepository(WhatsappWebhookRepository):
    """
    PgWhatsappWebhookRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, webhook):
        """add wa webhook to session"""

        self.__session.add(WebhookMapper.to_model(webhook))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get webhook"""

        webhook = await self.__session.get(WhatsappWebhookModel, id)

        if webhook:
            return WebhookMapper.to_domain(webhook)

        return None
