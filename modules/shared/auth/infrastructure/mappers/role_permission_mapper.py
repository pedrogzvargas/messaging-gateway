from sqlalchemy_models import RolePermissionModel
from modules.shared.auth.domain.entities import RolePermission


class RolePermissionMapper:

    @staticmethod
    def to_model(entity: RolePermission) -> RolePermissionModel:
        return RolePermissionModel(
            id=entity.id,
            role_id=entity.role_id,
            permission_id=entity.permission_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_domain(model: RolePermissionModel) -> RolePermission:
        return RolePermission(
            id=model.id,
            role_id=model.role_id,
            permission_id=model.permission_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
