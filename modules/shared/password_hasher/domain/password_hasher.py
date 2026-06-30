from abc import ABC
from abc import abstractmethod


class PasswordHasher(ABC):

    @abstractmethod
    def hash(self, password):
        """function to hash password"""
        pass

    @abstractmethod
    def verify(self, hashed_password, password):
        """function to verify password"""
        pass
