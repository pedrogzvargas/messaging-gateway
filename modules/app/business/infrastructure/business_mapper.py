from sqlalchemy_models import BusinessModel
from modules.app.business.domain import Business


class BusinessMapper:

    @staticmethod
    def to_model(entity: Business) -> BusinessModel:
        return BusinessModel(
            id=entity.id,
            customer_id=entity.customer_id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: BusinessModel) -> Business:
        return Business(
            id=model.id,
            customer_id=model.customer_id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
