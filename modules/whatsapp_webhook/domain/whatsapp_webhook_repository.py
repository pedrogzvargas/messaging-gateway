from uuid import UUID
from abc import ABC
from abc import abstractmethod


class WhatsappWebhookRepository(ABC):
    """
    Repository for WhatsApp webhook database table operations
    """

    @abstractmethod
    async def add(self, webhook):
        """add WhatsApp webhook to session"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get WhatsApp webhook"""
        pass
