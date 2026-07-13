from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ConversationItem:
    id: UUID
    channel: str
    provider_id: str
    display_name: str
    created_at: datetime
    updated_at: datetime
