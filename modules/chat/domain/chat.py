from abc import ABC
from abc import abstractmethod


class Chat(ABC):

    @abstractmethod
    async def process_message(self, user_id: str, message: str):
        pass
