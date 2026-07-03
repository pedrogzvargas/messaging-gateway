from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.webhook_event.domain import WebhookEventRepository
from sqlalchemy_models import WebhookEventModel
from .webhook_mapper import WebhookMapper


class PgWebhookEventRepository(WebhookEventRepository):
    """
    PgWebhookEventRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, webhook):
        """add wa webhook to session"""

        self.__session.add(WebhookMapper.to_model(webhook))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get webhook"""

        webhook = await self.__session.get(WebhookEventModel, id)

        if webhook:
            return WebhookMapper.to_domain(webhook)

        return None
