from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ChannelAccountItem:
    id: UUID
    channel: str
    business: str
    provider_id: str
    created_at: datetime
    updated_at: datetime
