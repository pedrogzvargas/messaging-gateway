from abc import ABC
from abc import abstractmethod


class DBSessionCreator(ABC):
    """
    Port to database session creator
    """

    @abstractmethod
    def create(self):
        """function to crate database session"""
        pass
