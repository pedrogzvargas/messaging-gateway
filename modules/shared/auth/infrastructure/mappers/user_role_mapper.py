from sqlalchemy_models import UserRoleModel
from modules.shared.auth.domain.entities import UserRole


class UserRoleMapper:

    @staticmethod
    def to_model(entity: UserRole) -> UserRoleModel:
        return UserRoleModel(
            id=entity.id,
            user_id=entity.user_id,
            role_id=entity.role_id,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_domain(model: UserRoleModel) -> UserRole:
        return UserRole(
            id=model.id,
            user_id=model.user_id,
            role_id=model.role_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
