from abc import ABC
from abc import abstractmethod


class EventBus(ABC):
    """
    Port for event bus creator
    """

    @abstractmethod
    async def publish(self, domain_events):
        """function to publish domain events"""
        pass
