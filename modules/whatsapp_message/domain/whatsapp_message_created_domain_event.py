from uuid import UUID
from datetime import datetime
from modules.shared.bus.event.domain import DomainEvent


class WhatsappMessageCreatedDomainEvent(DomainEvent):

    def __init__(
        self,
        aggregate_id: UUID,
        conversation_id: UUID,
        role: str,
        wa_message_id: str,
        from_number: str,
        to_number: str,
        message_type: str,
        message_text: str,
        direction: str,
        timestamp: datetime,
        raw_payload: dict,
        event_id=None,
        occurred_on=None,
    ):
        super().__init__(aggregate_id=aggregate_id, event_id=event_id, occurred_on=occurred_on)
        self.__conversation_id = conversation_id
        self.__role = role
        self.__wa_message_id = wa_message_id
        self.__from_number = from_number
        self.__to_number = to_number
        self.__message_type = message_type
        self.__message_text = message_text
        self.__direction = direction
        self.__timestamp = timestamp
        self.__raw_payload = raw_payload

    def event_name(self):
        return "app.whatsapp_message.created"

    def to_primitives(self):
        return dict(
            conversation_id=self.__conversation_id,
            role=self.__role,
            wa_message_id=self.__wa_message_id,
            from_number=self.__from_number,
            to_number=self.__to_number,
            message_type=self.__message_type,
            message_text=self.__message_text,
            direction=self.__direction,
            timestamp=self.__timestamp,
            raw_payload=self.__raw_payload,
            aggregate_id=self.aggregate_id,
            event_id=self.event_id,
            event_name=self.event_name(),
            occurred_on=self.occurred_on,
        )

    def from_primitives(self, aggregate_id, body, event_id, occurred_on):
        return WhatsappMessageCreatedDomainEvent(
            conversation_id=body.get("conversation_id"),
            role=body.get("role"),
            wa_message_id=body.get("wa_message_id"),
            from_number=body.get("from_number"),
            to_number=body.get("to_number"),
            message_type=body.get("message_type"),
            message_text=body.get("message_text"),
            direction=body.get("direction"),
            timestamp=body.get("timestamp"),
            raw_payload=body.get("raw_payload"),
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
    def wa_message_id(self):
        return self.__wa_message_id

    @property
    def from_number(self):
        return self.__from_number

    @property
    def to_number(self):
        return self.__to_number

    @property
    def message_type(self):
        return self.__message_type

    @property
    def message_text(self):
        return self.__message_text

    @property
    def direction(self):
        return self.__direction

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def raw_payload(self):
        return self.__raw_payload
