from uuid import UUID
from abc import ABC
from abc import abstractmethod


class CustomerRepository(ABC):
    """
    Repository for customer table operations
    """

    @abstractmethod
    async def get(self, id: UUID):
        """get customer by id"""
        pass

    @abstractmethod
    async def patch(self, customer):
        """patch customer"""
        pass
