from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CustomerNotificationItem:
    id: UUID
    customer_id: UUID
    content: str
    status: str
    created_at: datetime
    updated_at: datetime
