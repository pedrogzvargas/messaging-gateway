from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class ContactQueryParams(BaseModel):
    channel: Optional[str] = Query(default=None, required=False, description="channel name")
    display_name: Optional[str] = Query(default=None, required=False, description="display name")
    provider_id: Optional[str] = Query(default=None, required=False, description="provider id")
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)
