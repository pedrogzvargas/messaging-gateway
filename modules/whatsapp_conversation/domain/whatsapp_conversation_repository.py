from uuid import UUID
from abc import ABC
from abc import abstractmethod


class WhatsappConversationRepository(ABC):
    """
    Repository for WhatsApp conversation database table operations
    """

    @abstractmethod
    async def add(self, customer):
        """add WhatsApp conversation to session"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple WhatsApp conversation search"""
        pass

    @abstractmethod
    def all(self):
        """list all WhatsApp conversation"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get WhatsApp conversation"""
        pass

    @abstractmethod
    async def get_by_phone(self, phone: str):
        """get WhatsApp conversation by phone"""
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        """delete WhatsApp conversation"""
        pass
