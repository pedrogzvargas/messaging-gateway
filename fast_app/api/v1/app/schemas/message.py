from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class MessageQueryParams(BaseModel):
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
