from uuid import uuid4
from datetime import datetime
from abc import ABC
from abc import abstractmethod


class DomainEvent(ABC):
    """
    Port for domain event
    """

    def __init__(self, aggregate_id, event_id=None, occurred_on=None):
        self.__aggregate_id = aggregate_id
        self.__event_id = event_id or uuid4()
        self.__occurred_on = occurred_on or datetime.now()

    @abstractmethod
    def event_name(self):
        """function to create event name"""
        pass

    @abstractmethod
    def to_primitives(self):
        pass

    @abstractmethod
    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        pass

    @property
    def aggregate_id(self):
        return self.__aggregate_id

    @property
    def event_id(self):
        return self.__event_id

    @property
    def occurred_on(self):
        return self.__occurred_on
