from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.auth.domain.exceptions import ExpiredTokenError
from modules.shared.auth.domain.exceptions import InvalidTokenError
from modules.shared.environ.domain import Environ
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.domain.repositories import SessionRepository
from modules.shared.auth.application import Logout
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.auth.infrastructure.repositories import PostgresRefreshTokenRepository
from modules.shared.auth.infrastructure.repositories import PostgresSessionRepository


class LogoutController:
    """
    Class controller to logout
    """

    def __init__(
        self,
        session: AsyncSession,
        refresh_token_repository: RefreshTokenRepository | None = None,
        session_repository: SessionRepository | None = None,
        unit_of_work: UnitOfWork | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            token_handler: class to create token
            environ: environ variable reader
        """

        self.__session = session
        self.__refresh_token_repository = refresh_token_repository or PostgresRefreshTokenRepository(
            session=self.__session)
        self.__session_repository = session_repository or PostgresSessionRepository(session=self.__session)
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__environ = environ or PyEnviron()

    async def logout(self, jti: UUID):
        try:
            logout = Logout(
                unit_of_work=self.__unit_of_work,
                refresh_token_repository=self.__refresh_token_repository,
                session_repository=self.__session_repository,
            )
            await logout.logout(jti=jti)
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
            }, status.HTTP_200_OK

        except ExpiredTokenError as ex:
            response = {
                "success": False,
                "message": f"{messages.EXPIRED_TOKEN}",
            }, status.HTTP_401_UNAUTHORIZED
            return response

        except InvalidTokenError as ex:
            response = {
                "success": False,
                "message": f"{messages.INVALID_TOKEN}",
            }, status.HTTP_400_BAD_REQUEST
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
