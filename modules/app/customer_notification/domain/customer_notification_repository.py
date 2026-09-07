from abc import ABC
from abc import abstractmethod
from modules.shared.http.infrastructure import PageResult


class CustomerNotificationRepository(ABC):
    """
    Repository for customer_notification table operations
    """

    @abstractmethod
    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult:
        """simple customer notification search"""
        pass
