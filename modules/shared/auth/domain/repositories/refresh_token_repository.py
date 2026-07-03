from uuid import UUID
from abc import ABC
from abc import abstractmethod


class RefreshTokenRepository(ABC):
    """
    Repository for refresh token database table operations
    """

    @abstractmethod
    async def add(self, refresh_token):
        """add refresh_token to session"""
        pass

    @abstractmethod
    async def get(self, id: UUID):
        """get refresh_token"""
        pass

    async def patch(self, refresh_token):
        """patch refresh token method"""
        pass
