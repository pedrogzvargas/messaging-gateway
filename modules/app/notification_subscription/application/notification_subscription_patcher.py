from uuid import UUID
from modules.app.notification_subscription.domain import NotificationSubscription
from modules.app.notification_subscription.domain import NotificationSubscriptionRepository
from modules.app.notification_subscription.domain.exceptions import NotificationSubscriptionDoesNotExist
from modules.shared.persistence.domain import UnitOfWork


class NotificationSubscriptionPatcher:
    """
    Class to patch the NotificationSubscription of a given session
    """

    def __init__(self, unit_of_work: UnitOfWork, notification_subscription_repository: NotificationSubscriptionRepository):
        self.__unit_of_work = unit_of_work
        self.__notification_subscription_repository = notification_subscription_repository

    async def patch(self, session_id: UUID, data: dict) -> NotificationSubscription:
        notification_subscription = await self.__notification_subscription_repository.get_by_session_id(session_id=session_id)

        if not notification_subscription:
            raise NotificationSubscriptionDoesNotExist(f"NotificationSubscription for session:{session_id} not found")

        notification_subscription.patch(data=data)

        async with self.__unit_of_work:
            await self.__notification_subscription_repository.patch(notification_subscription)

        return notification_subscription
