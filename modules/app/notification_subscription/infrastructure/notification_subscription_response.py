from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class NotificationSubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    session_id: UUID
    payload: dict
    enabled: bool
    created_at: datetime
    updated_at: datetime
