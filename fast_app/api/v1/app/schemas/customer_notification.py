from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class CustomerNotificationQueryParams(BaseModel):
    status: Optional[str] = Query(default=None, required=False, description="customer notification status")
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)
