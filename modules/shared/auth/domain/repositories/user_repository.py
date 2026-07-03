from uuid import UUID
from abc import ABC
from abc import abstractmethod


class UserRepository(ABC):
    """
    Repository for user database table operations
    """

    @abstractmethod
    async def add(self, user):
        """add user to session"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get user"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str):
        """get user by email"""
        pass

    @abstractmethod
    async def patch(self, user):
        """patch user"""
        pass
