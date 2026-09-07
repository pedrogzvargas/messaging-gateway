from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class FaqItem:
    id: UUID
    business_id: UUID
    question: str
    answer: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
