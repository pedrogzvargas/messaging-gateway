from uuid import UUID
from abc import ABC
from abc import abstractmethod
from modules.shared.http.infrastructure import PageResult


class FaqRepository(ABC):

    @abstractmethod
    async def get(self, id: UUID):
        """get faq"""
        pass

    @abstractmethod
    async def get_by_fields(self, **fields):
        """get prompt by fields"""
        pass

    @abstractmethod
    async def add(self, faq):
        """add faq to session"""
        pass

    async def patch(self, faq):
        """patch faq"""
        pass

    @abstractmethod
    async def search(self, question: str, limit: int = 2):
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult:
        """simple faq search"""
        pass

    @abstractmethod
    async def get_business_id_by_user_id(self, user_id: UUID):
        """get the business id owned by the given user"""
        pass
