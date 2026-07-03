from uuid import UUID
from abc import ABC
from abc import abstractmethod


class UserRoleRepository(ABC):
    """
    Repository for user role database table operations
    """

    @abstractmethod
    async def list_by_user_id(self, user_id: UUID):
        """list role by user id"""
        pass
