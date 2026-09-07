from uuid import UUID
from abc import ABC
from abc import abstractmethod
from modules.shared.http.infrastructure import PageResult


class BusinessPromptRepository(ABC):
    """
    Repository for business prompt table operations
    """

    @abstractmethod
    async def get(self, id: UUID):
        """get business prompt by id"""
        pass

    @abstractmethod
    async def get_by_fields(self, **fields):
        """get prompt by fields"""
        pass

    @abstractmethod
    async def patch(self, business_prompt):
        """patch business prompt"""
        pass

    @abstractmethod
    async def list_by_business_id(self, business_id: UUID):
        """list business prompts"""
        pass

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult:
        """simple business prompt search"""
        pass

    @abstractmethod
    async def get_business_id_by_user_id(self, user_id: UUID):
        """get the business id owned by the given user"""
        pass
