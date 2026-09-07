from uuid import UUID
from datetime import datetime
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

    async def get_detail(self, id: UUID, business_id: UUID | None = None):
        """get conversation detail, optionally scoped to a business"""
        pass

    @abstractmethod
    async def get_by_fields(self, **fields):
        """get conversation by fields"""
        pass

    @abstractmethod
    async def get_business_id_by_user_id(self, user_id: UUID):
        """get the business id owned by the given user"""
        pass

    async def get_business_id_by_conversation_id(self, conversation_id: UUID):
        """get the business id owned by the given conversation"""
        pass

    @abstractmethod
    async def count_by_business_id(self, business_id: UUID, since: datetime | None = None) -> int:
        """count conversations owned by the given business, optionally created since a given datetime"""
        pass
