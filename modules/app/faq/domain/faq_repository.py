from abc import ABC
from abc import abstractmethod


class FaqRepository(ABC):

    @abstractmethod
    async def search(self, question: str, limit: int = 2):
        pass
