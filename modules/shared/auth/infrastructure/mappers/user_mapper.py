from sqlalchemy_models import UserModel
from modules.shared.auth.domain.entities import User


class UserMapper:

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=entity.email,
            username=entity.username,
            password=entity.password,
            is_active=entity.is_active,
        )

    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            password=model.password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
