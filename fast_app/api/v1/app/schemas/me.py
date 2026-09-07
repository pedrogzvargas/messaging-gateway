from pydantic import BaseModel
from modules.app.customer.infrastructure import CustomerResponse


class MeResponse(BaseModel):
    success: bool
    message: str
    data: CustomerResponse


class PatchCustomer(BaseModel):
    name: str
    last_name: str
    second_last_name: str | None
