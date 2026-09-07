from uuid import UUID
from datetime import datetime


class Faq:

    def __init__(
        self,
        id: UUID,
        business_id: UUID,
        question: str,
        answer: str,
        embedding: list[float],
        is_active: bool,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.business_id = business_id
        self.question = question
        self.answer = answer
        self.embedding = embedding
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def create(
        id: UUID,
        business_id: UUID,
        question: str,
        answer: str,
        embedding: list[float],
        is_active: bool,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):

        return Faq(
            id=id,
            business_id=business_id,
            question=question,
            answer=answer,
            embedding=embedding,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at,
        )

    def patch(self, data: dict):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
