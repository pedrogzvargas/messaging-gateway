from uuid import UUID
from abc import ABC
from abc import abstractmethod


class ConversationRepository(ABC):
    """
    Repository for conversation database table operations
    """

    @abstractmethod
    async def add(self, customer):
        """add conversation to session"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get conversation"""
        pass

    @abstractmethod
    async def get_by_fields(self, **fields):
        """get conversation by fields"""
        pass
