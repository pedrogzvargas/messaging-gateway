from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_id: UUID
    details: str
    status: str
    created_at: datetime
    updated_at: datetime
