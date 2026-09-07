from sqlalchemy_models import FAQModel
from modules.app.faq.domain import Faq


class FaqMapper:

    @staticmethod
    def to_model(entity: Faq) -> FAQModel:
        return FAQModel(
            id=entity.id,
            business_id=entity.business_id,
            question=entity.question,
            answer=entity.answer,
            embedding=entity.embedding,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: FAQModel) -> Faq:
        return Faq(
            id=model.id,
            business_id=model.business_id,
            question=model.question,
            answer=model.answer,
            embedding=model.embedding,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
