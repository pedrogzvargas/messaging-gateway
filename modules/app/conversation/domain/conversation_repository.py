from uuid import UUID
from abc import ABC
from abc import abstractmethod
from modules.shared.http.infrastructure import PageResult


class ConversationRepository(ABC):
    """
    Repository for conversation database table operations
    """

    @abstractmethod
    async def add(self, customer):
        """add conversation to session"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult:
        """simple conversation search"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get conversation"""
        pass

    async def get_detail(self, id: UUID):
        """get conversation detail"""
        pass

    @abstractmethod
    async def get_by_fields(self, **fields):
        """get conversation by fields"""
        pass
