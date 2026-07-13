from uuid import UUID
from datetime import datetime


class Contact:

    def __init__(
        self,
        id: UUID,
        channel_account_id: UUID,
        provider_id: str,
        display_name: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.channel_account_id = channel_account_id
        self.provider_id = provider_id
        self.display_name = display_name
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        channel_account_id: UUID,
        provider_id: str,
        display_name: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        contact = Contact(
            id=id,
            channel_account_id=channel_account_id,
            provider_id=provider_id,
            display_name=display_name,
            created_at=created_at,
            updated_at=updated_at,
        )

        return contact
