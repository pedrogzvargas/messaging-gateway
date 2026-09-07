from uuid import UUID
from pydantic import BaseModel
from pydantic import ConfigDict


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    last_name: str
    second_last_name: str | None
