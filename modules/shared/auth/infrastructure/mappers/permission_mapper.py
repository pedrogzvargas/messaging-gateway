from sqlalchemy_models import PermissionModel
from modules.shared.auth.domain.entities import Permission


class PermissionMapper:

    @staticmethod
    def to_model(entity: Permission) -> PermissionModel:
        return PermissionModel(
            id=entity.id,
            name=entity.name,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_domain(model: PermissionModel) -> Permission:
        return Permission(
            id=model.id,
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
