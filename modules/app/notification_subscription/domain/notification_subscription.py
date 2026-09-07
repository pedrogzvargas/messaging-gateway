from uuid import UUID
from datetime import datetime


class NotificationSubscription:

    PATCHABLE_FIELDS = {"enabled"}

    def __init__(
        self,
        id: UUID,
        session_id: UUID,
        payload: dict,
        enabled: bool,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.session_id = session_id
        self.payload = payload
        self.enabled = enabled
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        session_id: UUID,
        payload: dict,
        enabled: bool = True,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):

        return NotificationSubscription(
            id=id,
            session_id=session_id,
            payload=payload,
            enabled=enabled,
            created_at=created_at,
            updated_at=updated_at,
        )

    def patch(self, data: dict):
        for attr, value in data.items():
            if attr in self.PATCHABLE_FIELDS:
                setattr(self, attr, value)
