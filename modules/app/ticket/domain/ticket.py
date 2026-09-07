from uuid import UUID
from datetime import datetime


class Ticket:

    PATCHABLE_FIELDS = {"status"}

    def __init__(
        self,
        id: UUID,
        customer_id: UUID,
        details: str,
        status: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.customer_id = customer_id
        self.details = details
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        customer_id: UUID,
        details: str,
        status: str = "open",
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):

        return Ticket(
            id=id,
            customer_id=customer_id,
            details=details,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

    def patch(self, data: dict):
        for attr, value in data.items():
            if attr in self.PATCHABLE_FIELDS:
                setattr(self, attr, value)
