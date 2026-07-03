from abc import ABC
from abc import abstractmethod


class EntitySerializer(ABC):

    @abstractmethod
    def dump(self, entity, many=False):
        """function to serialize entity"""
        pass
