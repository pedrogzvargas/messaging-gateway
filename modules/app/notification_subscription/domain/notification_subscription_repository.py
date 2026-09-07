from uuid import UUID
from abc import ABC
from abc import abstractmethod


class NotificationSubscriptionRepository(ABC):
    """
    Repository for notification_subscription table operations
    """

    @abstractmethod
    async def get(self, id: UUID):
        """get notification_subscription by id"""
        pass

    @abstractmethod
    async def get_by_session_id(self, session_id: UUID):
        """get notification_subscription by session id"""
        pass

    @abstractmethod
    async def add(self, notification_subscription):
        """add notification_subscription to session"""
        pass

    @abstractmethod
    async def patch(self, notification_subscription):
        """patch notification_subscription"""
        pass
