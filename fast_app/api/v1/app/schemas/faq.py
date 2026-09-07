from uuid import UUID
from pydantic import BaseModel
from fastapi import Query
from typing import Optional


class FaqQueryParams(BaseModel):
    question: Optional[str] = Query(default=None, required=False, description="question")
    limit: Optional[int] = Query(ge=1, le=500000, required=False, default=10)
    page: Optional[int] = Query(ge=1, le=500000, required=False, default=1)


class Faq(BaseModel):
    id: UUID
    question: str
    answer: str
    is_active: bool


class PatchFaq(BaseModel):
    question: str
    answer: str
    is_active: bool
