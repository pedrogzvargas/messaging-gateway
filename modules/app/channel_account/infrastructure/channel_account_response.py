from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class ChannelAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel: str
    business: str
    provider_id: str
    created_at: datetime
    updated_at: datetime
