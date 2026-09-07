from uuid import UUID
from typing import Any
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    role: str
    message_id: str
    message_type: str
    message: str
    direction: str
    timestamp: datetime
    payload: dict[str, Any]
