from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.app.notification_subscription.domain import NotificationSubscriptionRepository
from sqlalchemy_models import NotificationSubscriptionModel
from .notification_subscription_mapper import NotificationSubscriptionMapper


class PgNotificationSubscriptionRepository(NotificationSubscriptionRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, id: UUID):
        """get notification_subscription"""

        notification_subscription = await self.__session.get(NotificationSubscriptionModel, id)

        if notification_subscription:
            return NotificationSubscriptionMapper.to_domain(notification_subscription)

        return None

    async def get_by_session_id(self, session_id: UUID):
        """get notification_subscription by session id"""

        stmt = select(NotificationSubscriptionModel).where(NotificationSubscriptionModel.session_id == session_id)
        query_result = await self.__session.execute(stmt)
        notification_subscription = query_result.scalar_one_or_none()

        if notification_subscription:
            return NotificationSubscriptionMapper.to_domain(notification_subscription)

        return None

    async def add(self, notification_subscription):
        """add notification_subscription to session"""

        self.__session.add(NotificationSubscriptionMapper.to_model(notification_subscription))
        await self.__session.flush()

    async def patch(self, notification_subscription):
        """patch notification_subscription"""

        await self.__session.merge(NotificationSubscriptionMapper.to_model(notification_subscription))
