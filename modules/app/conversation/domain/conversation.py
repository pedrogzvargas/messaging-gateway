from uuid import UUID
from datetime import datetime


class Conversation:

    def __init__(
        self,
        id: UUID,
        channel_account_id: UUID,
        contact_id: UUID,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.channel_account_id = channel_account_id
        self.contact_id = contact_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        channel_account_id: UUID,
        contact_id: UUID,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        conversation = Conversation(
            id=id,
            channel_account_id=channel_account_id,
            contact_id=contact_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return conversation
