from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class BusinessPromptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    business_id: UUID
    key: str
    description: str
    content: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
