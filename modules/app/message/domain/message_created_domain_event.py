from uuid import UUID
from datetime import datetime
from modules.shared.bus.event.domain import DomainEvent


class MessageCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id: UUID,
        conversation_id: UUID,
        role: str,
        message_id: str,
        message_type: str,
        message: str,
        direction: str,
        timestamp: datetime,
        payload: dict,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__conversation_id = conversation_id
        self.__role = role
        self.__message_id = message_id
        self.__message_type = message_type
        self.__message = message
        self.__direction = direction
        self.__timestamp = timestamp
        self.__payload = payload

    def event_name(self):
        return "app.message.created"

    def to_primitives(self):
        return dict(
            conversation_id=self.__conversation_id,
            role=self.__role,
            message_id=self.__message_id,
            message_type=self.__message_type,
            message=self.__message,
            direction=self.__direction,
            timestamp=self.__timestamp,
            payload=self.__payload,
            aggregate_id=self.aggregate_id,
            event_id=self.event_id,
            event_name=self.event_name(),
            occurred_on=self.occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return MessageCreatedDomainEvent(
            conversation_id=body.get("conversation_id"),
            role=body.get("role"),
            message_id=body.get("message_id"),
            message_type=body.get("message_type"),
            message=body.get("message"),
            direction=body.get("direction"),
            timestamp=body.get("timestamp"),
            payload=body.get("payload"),
            aggregate_id=aggregate_id,
            event_id=event_id,
            occurred_on=occurred_on,
        )

    @property
    def conversation_id(self):
        return self.__conversation_id

    @property
    def role(self):
        return self.__role

    @property
    def message_id(self):
        return self.__message_id

    @property
    def message_type(self):
        return self.__message_type

    @property
    def message(self):
        return self.__message

    @property
    def direction(self):
        return self.__direction

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def payload(self):
        return self.__payload
