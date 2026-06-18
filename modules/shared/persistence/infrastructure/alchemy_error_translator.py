from sqlalchemy.exc import IntegrityError, OperationalError
from modules.shared.persistence.domain import UniqueConstraintError
from modules.shared.persistence.domain import DatabaseError


class AlchemyErrorTranslator:

    @staticmethod
    def translate(exc: Exception) -> Exception:
        if isinstance(exc, IntegrityError):
            if "unique" in str(exc).lower():
                return UniqueConstraintError("Unique constraint violated")
            return DatabaseError("Integrity error")

        if isinstance(exc, OperationalError):
            return DatabaseError("Database unavailable")

        return exc
