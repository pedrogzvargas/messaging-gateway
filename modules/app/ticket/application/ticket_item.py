from uuid import UUID
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TicketItem:
    id: UUID
    customer_id: UUID
    details: str
    status: str
    created_at: datetime
    updated_at: datetime
