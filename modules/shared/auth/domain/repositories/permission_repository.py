from abc import ABC
from abc import abstractmethod
from typing import List


class PermissionRepository(ABC):
    """
    Repository for permission database table operations
    """

    @abstractmethod
    async def list_by_ids(self, ids: List):
        """list permission by role id"""
        pass
