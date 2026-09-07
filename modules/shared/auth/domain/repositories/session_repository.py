from uuid import UUID
from abc import ABC
from abc import abstractmethod


class SessionRepository(ABC):
    """
    Repository for session database table operations
    """

    @abstractmethod
    async def add(self, session):
        """add session to db session"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get session"""
        pass

    async def patch(self, session):
        """patch session method"""
        pass
