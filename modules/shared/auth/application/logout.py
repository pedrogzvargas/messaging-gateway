from uuid import UUID
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.domain.repositories import SessionRepository
from modules.shared.persistence.domain import UnitOfWork


class Logout:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        refresh_token_repository: RefreshTokenRepository,
        session_repository: SessionRepository,
    ):
        self.__refresh_token_repository = refresh_token_repository
        self.__session_repository = session_repository
        self.__unit_of_work = unit_of_work

    async def logout(self, jti: UUID):
        refresh_token = await self.__refresh_token_repository.get(id=jti)
        refresh_token.patch({"revoked": True})

        session = await self.__session_repository.get(id=refresh_token.session_id)
        session.patch({"revoked": True})

        async with self.__unit_of_work:
            await self.__refresh_token_repository.patch(refresh_token=refresh_token)
            await self.__session_repository.patch(session=session)
