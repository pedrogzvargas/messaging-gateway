from uuid import UUID
from datetime import datetime


class Business:

    def __init__(
        self,
        id: UUID,
        customer_id: UUID,
        name: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.customer_id = customer_id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
