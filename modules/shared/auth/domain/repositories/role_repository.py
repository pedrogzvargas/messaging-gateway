from abc import ABC
from abc import abstractmethod
from typing import List


class RoleRepository(ABC):
    """
    Repository for role database table operations
    """

    @abstractmethod
    async def list_by_ids(self, ids: List):
        """list role by user id"""
        pass
