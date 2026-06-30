from uuid import UUID
from datetime import datetime


class ChannelAccount:

    def __init__(
        self,
        id: UUID,
        channel_id: UUID,
        business_id: UUID,
        provider_id: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.channel_id = channel_id
        self.business_id = business_id
        self.provider_id = provider_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        channel_id: UUID,
        business_id: UUID,
        provider_id: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        channel_account = ChannelAccount(
            id=id,
            channel_id=channel_id,
            business_id=business_id,
            provider_id=provider_id,
            created_at=created_at,
            updated_at=updated_at,
        )

        return channel_account
