from abc import ABC
from abc import abstractmethod


class TokenHandler(ABC):

    @abstractmethod
    def encode(self, payload):
        """function to encode token"""
        pass

    @abstractmethod
    def decode(self, token):
        """function to decode token"""
        pass
