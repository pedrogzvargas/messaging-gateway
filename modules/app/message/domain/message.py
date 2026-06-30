from uuid import UUID
from datetime import datetime
from modules.shared.aggregate_root.domain import AggregateRoot
from .message_created_domain_event import MessageCreatedDomainEvent


class Message(AggregateRoot):

    def __init__(
        self,
        id: UUID,
        conversation_id: UUID,
        role: str,
        message_id: str,
        message_type: str,
        message: str,
        direction: str,
        timestamp: datetime,
        payload: dict,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__()
        self.id = id
        self.conversation_id = conversation_id
        self.role = role
        self.message_id = message_id
        self.message_type = message_type
        self.message = message
        self.direction = direction
        self.timestamp = timestamp
        self.payload = payload
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        conversation_id: UUID,
        role: str,
        message_id: str,
        message_type: str,
        message: str,
        direction: str,
        timestamp: datetime,
        payload: dict,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        message_entity = Message(
            id=id,
            conversation_id=conversation_id,
            role=role,
            message_id=message_id,
            message_type=message_type,
            message=message,
            direction=direction,
            timestamp=timestamp,
            payload=payload,
            created_at=created_at,
            updated_at=updated_at,
        )

        message_entity.record(
            MessageCreatedDomainEvent(
                aggregate_id=id,
                conversation_id=conversation_id,
                role=role,
                message_id=message_id,
                message_type=message_type,
                message=message,
                direction=direction,
                timestamp=timestamp,
                payload=payload,
            )
        )

        return message_entity
