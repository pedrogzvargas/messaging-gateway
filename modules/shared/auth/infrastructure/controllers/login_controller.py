from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import AuthAttemptHandler
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import WrongCredentials
from modules.shared.auth.domain import LockedAccount
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.domain.repositories import UserRoleRepository
from modules.shared.auth.domain.repositories import RoleRepository
from modules.shared.auth.domain.repositories import RolePermissionRepository
from modules.shared.auth.domain.repositories import PermissionRepository
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.environ.domain import Environ
from modules.shared.serializer.domain import EntitySerializer
from modules.shared.auth.application import Login
from modules.shared.auth.infrastructure.repositories import PostgresRefreshTokenRepository
from modules.shared.auth.infrastructure.repositories import PostgresUserRepository
from modules.shared.auth.infrastructure.repositories import PostgresUserRoleRepository
from modules.shared.auth.infrastructure.repositories import PostgresRoleRepository
from modules.shared.auth.infrastructure.repositories import PostgresRolePermissionRepository
from modules.shared.auth.infrastructure.repositories import PostgresPermissionRepository
from modules.shared.auth.infrastructure import LoginSchema
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.serializer.infrastructure.marshmallow import MarshmallowEntitySerializer
from modules.shared.password_hasher.infrastructure import Argon2PasswordHasher
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.shared.auth.infrastructure import JwtTokenHandler
from modules.shared.auth.infrastructure import RedisAuthAttemptHandler


class LoginController:
    """
    Class controller to login
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        user_repository: UserRepository | None = None,
        user_role_repository: UserRoleRepository | None = None,
        role_repository: RoleRepository | None = None,
        role_permission_repository: RolePermissionRepository | None = None,
        permission_repository: PermissionRepository | None = None,
        refresh_token_repository: RefreshTokenRepository | None = None,
        password_hasher: PasswordHasher | None = None,
        token_handler: TokenHandler | None = None,
        auth_attempt_handler: AuthAttemptHandler | None = None,
        entity_serializer: EntitySerializer | None = None,
        environ: Environ | None = None
    ):
        """
        Args:
            user_repository: repository for user database table operations
            password_hasher: class to hash and verify password
            token_handler: class to create token
            entity_serializer: entity serializer
            environ: environ variable reader
        """

        self.__session = session
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)
        self.__user_role_repository = user_role_repository or PostgresUserRoleRepository(session=self.__session)
        self.__role_repository = role_repository or PostgresRoleRepository(session=self.__session)
        self.__role_permission_repository = role_permission_repository or PostgresRolePermissionRepository(session=self.__session)
        self.__permission_repository = permission_repository or PostgresPermissionRepository(session=self.__session)
        self.__refresh_token_repository = refresh_token_repository or PostgresRefreshTokenRepository(session=self.__session)
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__token_handler = token_handler or JwtTokenHandler(self.__environ.get_str("SECRET_KEY"))
        self.__auth_attempt_handler = auth_attempt_handler or RedisAuthAttemptHandler(
            Redis(
                host=self.__environ.get_str("REDIS_HOST", "localhost"),
                port=self.__environ.get_int("REDIS_PORT", 6379),
                decode_responses=True
            ), environ=self.__environ
        )
        self.__entity_serializer = entity_serializer or MarshmallowEntitySerializer(schema=LoginSchema())

    async def login(self, body: dict):
        try:
            login = Login(
                unit_of_work=self.__unit_of_work,
                user_repository=self.__user_repository,
                user_role_repository=self.__user_role_repository,
                role_repository=self.__role_repository,
                permission_repository=self.__permission_repository,
                role_permission_repository=self.__role_permission_repository,
                refresh_token_repository=self.__refresh_token_repository,
                password_hasher=self.__password_hasher,
                token_handler=self.__token_handler,
                auth_attempt_handler=self.__auth_attempt_handler,
            )
            access_token, refresh_token = await login.login(email=body.get("email"), password=body.get("password"))
            login_response = self.__entity_serializer(dict(access_token=access_token, refresh_token=refresh_token))
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": login_response
            }, status.HTTP_200_OK

        except (UserDoesNotExist, WrongCredentials) as ex:
            response = {
                "success": False,
                "message": f"{messages.WRONG_CREDENTIALS}",
                "data": {}
            }, status.HTTP_400_BAD_REQUEST
            return response

        except LockedAccount as ex:
            response = {
                "success": False,
                "message": f"{messages.TOO_MANY_LOGIN_ATTEMPTS}",
                "data": {}
            }, status.HTTP_429_TOO_MANY_REQUESTS
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
