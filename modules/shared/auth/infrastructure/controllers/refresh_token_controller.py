from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.application import TokenRefresher
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.auth.domain.exceptions import ExpiredTokenError
from modules.shared.auth.domain.exceptions import InvalidTokenError
from modules.shared.environ.domain import Environ
from modules.shared.auth.infrastructure import LoginSchema
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.auth.infrastructure.repositories import PostgresRefreshTokenRepository
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.auth.infrastructure import JwtTokenHandler


class RefreshTokenController:
    """
    Class controller to refresh token
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        refresh_token_repository: RefreshTokenRepository | None = None,
        token_handler: TokenHandler | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            token_handler: class to create token
            entity_serializer: entity serializer
            environ: environ variable reader
        """

        self.__session = session
        self.__refresh_token_repository = refresh_token_repository or PostgresRefreshTokenRepository(
            session=self.__session)
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__token_handler = token_handler or JwtTokenHandler(self.__environ.get_str("SECRET_KEY"))
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=LoginSchema())

    async def refresh(self, body: dict):
        try:
            token_refresher = TokenRefresher(
                refresh_token_repository=self.__refresh_token_repository,
                unit_of_work=self.__unit_of_work,
                token_handler=self.__token_handler,
            )
            access_token, refresh_token = await token_refresher.refresh(token=body.get("refresh_token"))
            refresh_token_response = self.__entity_serializer(dict(access_token=access_token, refresh_token=refresh_token))
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": refresh_token_response
            }, status.HTTP_200_OK

        except ExpiredTokenError as ex:
            response = {
                "success": False,
                "message": f"{messages.EXPIRED_TOKEN}",
                "data": {}
            }, status.HTTP_401_UNAUTHORIZED
            return response

        except InvalidTokenError as ex:
            response = {
                "success": False,
                "message": f"{messages.INVALID_TOKEN}",
                "data": {}
            }, status.HTTP_400_BAD_REQUEST
            return response

        except Exception as ex:
            response = {
                "success": False,
                "message": messages.INTERNAL_SERVER_ERROR,
                "data": {}
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

        else:
            return response
