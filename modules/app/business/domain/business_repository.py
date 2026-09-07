from uuid import UUID
from abc import ABC
from abc import abstractmethod


class BusinessRepository(ABC):
    """
    Repository for business table operations
    """

    @abstractmethod
    async def get(self, id: UUID):
        """get business by id"""
        pass

    @abstractmethod
    async def get_by_customer_id(self, customer_id: UUID):
        """get business by customer id"""
        pass
