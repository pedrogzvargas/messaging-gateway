from abc import ABC
from abc import abstractmethod


class QuestionRepository(ABC):

    @abstractmethod
    async def search(self, question: str, limit: int = 2):
        pass
