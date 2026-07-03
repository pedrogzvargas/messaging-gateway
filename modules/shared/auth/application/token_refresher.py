from uuid import uuid4
from uuid import UUID
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain.exceptions import InvalidTokenError
from modules.shared.auth.domain.entities import RefreshToken


class TokenRefresher:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        refresh_token_repository: RefreshTokenRepository,
        token_handler: TokenHandler,
    ):

        self.__refresh_token_repository = refresh_token_repository
        self.__token_handler = token_handler
        self.__unit_of_work = unit_of_work

    async def refresh(self, token):
        refresh_token_payload = self.__token_handler.decode(token)
        user_id = refresh_token_payload.get("sub")
        token_type = refresh_token_payload.get("type")
        current_jti = refresh_token_payload.get("jti")

        if token_type != "refresh":
            raise InvalidTokenError("Invalid token")

        jti = uuid4()

        access_token_payload = dict(
            sub=str(user_id),
            jti=str(jti),
            type="access",
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=15),
        )

        refresh_token_payload = dict(
            sub=str(user_id),
            jti=str(jti),
            type="refresh",
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(hours=24),
        )

        current_refresh_token = await self.__refresh_token_repository.get(id=current_jti)

        if current_refresh_token.revoked:
            raise InvalidTokenError("Refresh token revoked")

        current_refresh_token.patch({"revoked": True})

        access_token = self.__token_handler.encode(payload=access_token_payload)
        refresh_token = self.__token_handler.encode(payload=refresh_token_payload)
        refresh_token_entity = RefreshToken.create(id=jti, user_id=UUID(user_id), jti=jti)

        async with self.__unit_of_work:
            await self.__refresh_token_repository.patch(refresh_token=current_refresh_token)
            await self.__refresh_token_repository.add(refresh_token=refresh_token_entity)

        return access_token, refresh_token
