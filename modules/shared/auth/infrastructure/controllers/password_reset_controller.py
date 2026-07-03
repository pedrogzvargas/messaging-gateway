from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from modules.shared.environ.domain import Environ
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.auth.domain.repositories import PasswordResetTokenRepository
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.application import PasswordReset
from modules.shared.auth.infrastructure.repositories import PostgresUserRepository
from modules.shared.auth.infrastructure.repositories import RedisPasswordResetTokenRepository
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.password_hasher.infrastructure import Argon2PasswordHasher
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


class PasswordResetController:
    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        user_repository: UserRepository | None = None,
        password_reset_token_repository: PasswordResetTokenRepository | None = None,
        password_hasher: PasswordHasher | None = None,
        environ: Environ | None = None
    ):
        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__user_repository = user_repository or PostgresUserRepository(session=self.__session)
        self.__password_reset_token_repository = password_reset_token_repository or RedisPasswordResetTokenRepository(
            redis=Redis(
                host="localhost",
                port=6379,
                decode_responses=True,
            )
        )
        self.__password_hasher = password_hasher or Argon2PasswordHasher()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)

    async def recover(self, body: dict):
        try:
            password_reset = PasswordReset(
                user_repository=self.__user_repository,
                unit_of_work=self.__unit_of_work,
                password_reset_token_repository=self.__password_reset_token_repository,
                password_hasher=self.__password_hasher,
            )

            await password_reset.reset(token=body.get("token"), password=body.get("password"))

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except UserDoesNotExist as ex:
            response = {
                "success": False,
                "message": f"{ex}",
                "data": {}
            }, status.HTTP_404_NOT_FOUND
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
