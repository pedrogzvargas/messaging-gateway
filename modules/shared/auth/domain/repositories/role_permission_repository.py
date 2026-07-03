from abc import ABC
from abc import abstractmethod
from typing import List


class RolePermissionRepository(ABC):
    """
    Repository for role permission database table operations
    """

    @abstractmethod
    async def list_by_role_ids(self, ids: List):
        """list role permission by role ids"""
        pass
