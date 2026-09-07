from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class BusinessPromptItem:
    id: UUID
    business_id: UUID
    key: str
    description: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
