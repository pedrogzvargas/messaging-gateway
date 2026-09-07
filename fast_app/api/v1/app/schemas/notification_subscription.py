from uuid import UUID
from pydantic import BaseModel


class NotificationSubscription(BaseModel):
    id: UUID
    payload: dict


class PatchNotificationSubscription(BaseModel):
    enabled: bool
