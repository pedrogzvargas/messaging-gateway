from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain.exceptions import InvalidTokenError
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.persistence.domain import UnitOfWork


class Logout:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        refresh_token_repository: RefreshTokenRepository,
        token_handler: TokenHandler,
    ):
        self.__refresh_token_repository = refresh_token_repository
        self.__token_handler = token_handler
        self.__unit_of_work = unit_of_work

    async def logout(self, token):
        refresh_token_payload = self.__token_handler.decode(token)
        jti = refresh_token_payload.get("jti")
        token_type = refresh_token_payload.get("type")

        if token_type != "refresh":
            raise InvalidTokenError("Invalid token")

        refresh_token = await self.__refresh_token_repository.get(id=jti)
        refresh_token.patch({"revoked": True})

        async with self.__unit_of_work:
            await self.__refresh_token_repository.patch(refresh_token=refresh_token)
