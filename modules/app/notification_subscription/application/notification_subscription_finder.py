from uuid import UUID
from modules.app.notification_subscription.domain import NotificationSubscriptionRepository
from modules.app.notification_subscription.domain.exceptions import NotificationSubscriptionDoesNotExist


class NotificationSubscriptionFinder:
    """
    Class to find the NotificationSubscription of a given session
    """

    def __init__(self, notification_subscription_repository: NotificationSubscriptionRepository):
        self.__notification_subscription_repository = notification_subscription_repository

    async def find(self, session_id: UUID):
        notification_subscription = await self.__notification_subscription_repository.get_by_session_id(session_id=session_id)

        if not notification_subscription:
            raise NotificationSubscriptionDoesNotExist(f"NotificationSubscription for session:{session_id} not found")

        return notification_subscription
