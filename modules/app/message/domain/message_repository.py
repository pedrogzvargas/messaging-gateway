from uuid import UUID
from abc import ABC
from abc import abstractmethod


class MessageRepository(ABC):
    """
    Repository for message database table operations
    """

    @abstractmethod
    async def add(self, customer):
        """add WhatsApp message to session"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple WhatsApp message search"""
        pass

    @abstractmethod
    def all(self):
        """list all WhatsApp message"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get WhatsApp message"""
        pass

    @abstractmethod
    async def list_by_conversation(self, conversation_id: UUID, limit: int = 10):
        """get WhatsApp message by conversation_id"""
        pass
