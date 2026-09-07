from uuid import UUID
from datetime import datetime


class BusinessPrompt:

    PATCHABLE_FIELDS = {"description", "content", "role", "is_active"}

    def __init__(
        self,
        id: UUID,
        business_id: UUID,
        key: str,
        description: str,
        content: str,
        role: str,
        is_active: bool,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.business_id = business_id
        self.key = key
        self.description = description
        self.content = content
        self.role = role
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    def patch(self, data: dict):
        for attr, value in data.items():
            if attr in self.PATCHABLE_FIELDS:
                setattr(self, attr, value)