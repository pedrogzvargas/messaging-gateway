from uuid import UUID
from datetime import datetime


class WhatsappConversation:

    def __init__(self, id: UUID, phone_number: str, created_at: datetime | None = None, updated_at: datetime | None = None):
        self.id = id
        self.phone_number = phone_number
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id: UUID, phone_number: str, created_at: datetime | None = None, updated_at: datetime | None = None):
        whatsapp_conversation = WhatsappConversation(
            id=id,
            phone_number=phone_number,
            created_at=created_at,
            updated_at=updated_at,
        )

        return whatsapp_conversation
