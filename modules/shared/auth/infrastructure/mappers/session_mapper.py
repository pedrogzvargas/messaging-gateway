from sqlalchemy_models import SessionModel
from modules.shared.auth.domain.entities import Session


class SessionMapper:

    @staticmethod
    def to_model(entity: Session) -> SessionModel:
        return SessionModel(
            id=entity.id,
            user_id=entity.user_id,
            revoked=entity.revoked,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def to_domain(model: SessionModel) -> Session:
        return Session(
            id=model.id,
            user_id=model.user_id,
            revoked=model.revoked,
            expires_at=model.expires_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
