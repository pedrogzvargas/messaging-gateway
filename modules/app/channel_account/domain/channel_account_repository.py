from uuid import UUID
from abc import ABC
from abc import abstractmethod
from modules.shared.http.infrastructure import PageResult


class ChannelAccountRepository(ABC):
    """
    Repository for channel account table operations
    """

    @abstractmethod
    async def get(self, id: UUID):
        """get channel account"""
        pass

    @abstractmethod
    async def get_by_provider_id(self, provider_id: str):
        """get channel account by provider id"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult:
        """simple conversation search"""
        pass
