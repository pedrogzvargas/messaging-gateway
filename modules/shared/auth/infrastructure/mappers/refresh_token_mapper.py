from sqlalchemy_models import RefreshTokenModel
from modules.shared.auth.domain.entities import RefreshToken


class RefreshTokenMapper:

    @staticmethod
    def to_model(entity: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            jti=entity.jti,
            revoked=entity.revoked,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            jti=model.jti,
            revoked=model.revoked,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
