from sqlalchemy_models import BusinessPromptModel
from modules.app.business_prompt.domain import BusinessPrompt


class BusinessPromptMapper:

    @staticmethod
    def to_domain(model: BusinessPromptModel) -> BusinessPrompt:
        return BusinessPrompt(
            id=model.id,
            business_id=model.business_id,
            key=model.key,
            description=model.description,
            content=model.content,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: BusinessPrompt) -> BusinessPromptModel:
        return BusinessPromptModel(
            id=entity.id,
            business_id=entity.business_id,
            key=entity.key,
            description=entity.description,
            content=entity.content,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
