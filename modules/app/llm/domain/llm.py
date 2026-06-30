from abc import ABC
from abc import abstractmethod


class LLM(ABC):

    @abstractmethod
    async def invoke(self, messages: list):
        pass
