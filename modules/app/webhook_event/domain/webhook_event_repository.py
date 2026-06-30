from uuid import UUID
from abc import ABC
from abc import abstractmethod


class WebhookEventRepository(ABC):
    """
    Repository for webhook event
    """

    @abstractmethod
    async def add(self, webhook):
        """add webhook to session"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get webhook"""
        pass
