from uuid import UUID
from abc import ABC
from abc import abstractmethod
from modules.shared.http.infrastructure import PageResult


class TicketRepository(ABC):
    """
    Repository for ticket table operations
    """

    @abstractmethod
    async def get(self, id: UUID):
        """get ticket by id"""
        pass

    @abstractmethod
    async def add(self, ticket):
        """add ticket to session"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult:
        """simple ticket search"""
        pass

    @abstractmethod
    async def patch(self, ticket):
        """patch ticket"""
        pass
