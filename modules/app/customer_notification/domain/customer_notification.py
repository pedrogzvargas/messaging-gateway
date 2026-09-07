from uuid import UUID
from datetime import datetime


class CustomerNotification:

    def __init__(
        self,
        id: UUID,
        customer_id: UUID,
        content: str,
        status: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.customer_id = customer_id
        self.content = content
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
