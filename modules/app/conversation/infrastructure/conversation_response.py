from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel: str
    provider_id: str
    display_name: str
    created_at: datetime
    updated_at: datetime
