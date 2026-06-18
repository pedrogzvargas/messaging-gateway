from uuid import UUID
from datetime import datetime
from modules.shared.aggregate_root.domain import AggregateRoot
from .whatsapp_message_created_domain_event import WhatsappMessageCreatedDomainEvent


class WhatsappMessage(AggregateRoot):

    def __init__(
        self,
        id: UUID,
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
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__()
        self.id = id
        self.conversation_id = conversation_id
        self.role = role
        self.wa_message_id = wa_message_id
        self.from_number = from_number
        self.to_number = to_number
        self.message_type = message_type
        self.message_text = message_text
        self.direction = direction
        self.timestamp = timestamp
        self.raw_payload = raw_payload
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
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
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        whatsapp_message = WhatsappMessage(
            id=id,
            conversation_id=conversation_id,
            role=role,
            wa_message_id=wa_message_id,
            from_number=from_number,
            to_number=to_number,
            message_type=message_type,
            message_text=message_text,
            direction=direction,
            timestamp=timestamp,
            raw_payload=raw_payload,
            created_at=created_at,
            updated_at=updated_at,
        )

        whatsapp_message.record(
            WhatsappMessageCreatedDomainEvent(
                aggregate_id=id,
                conversation_id=conversation_id,
                role=role,
                wa_message_id=wa_message_id,
                from_number=from_number,
                to_number=to_number,
                message_type=message_type,
                message_text=message_text,
                direction=direction,
                timestamp=timestamp,
                raw_payload=raw_payload,
            )
        )

        return whatsapp_message
