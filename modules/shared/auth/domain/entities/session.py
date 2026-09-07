from uuid import UUID
from datetime import datetime


class Session:

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        revoked: bool,
        expires_at: datetime,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id
        self.user_id = user_id
        self.revoked = revoked
        self.expires_at = expires_at
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(id, user_id, expires_at, revoked=False, created_at=None, updated_at=None):
        return Session(
            id=id,
            user_id=user_id,
            revoked=revoked,
            expires_at=expires_at,
            created_at=created_at,
            updated_at=updated_at,
        )

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
