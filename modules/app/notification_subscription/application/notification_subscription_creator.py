from uuid import UUID
from modules.app.notification_subscription.domain import NotificationSubscription
from modules.app.notification_subscription.domain import NotificationSubscriptionRepository
from modules.app.notification_subscription.domain.exceptions import NotificationSubscriptionAlreadyExist
from modules.shared.persistence.domain import UnitOfWork


class NotificationSubscriptionCreator:

    def __init__(self, unit_of_work: UnitOfWork, notification_subscription_repository: NotificationSubscriptionRepository):
        self.__unit_of_work = unit_of_work
        self.__notification_subscription_repository = notification_subscription_repository

    async def create(self, id: UUID, session_id: UUID, payload: dict, enabled: bool = True):

        if await self.__notification_subscription_repository.get(id=id):
            raise NotificationSubscriptionAlreadyExist(f"NotificationSubscription with id:{id} already exists")

        notification_subscription = NotificationSubscription.create(
            id=id,
            session_id=session_id,
            payload=payload,
            enabled=enabled,
        )

        async with self.__unit_of_work:
            await self.__notification_subscription_repository.add(notification_subscription)
