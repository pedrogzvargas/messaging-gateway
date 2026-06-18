from abc import ABC
from abc import abstractmethod


class MessageChannel(ABC):

    @abstractmethod
    async def send_message(self, identifier: str, message: str):
        pass
