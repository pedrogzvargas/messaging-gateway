import smtplib
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from modules.shared.environ.domain import Environ
from modules.shared.http.domain import status
from modules.shared.http.domain import messages
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.auth.domain.repositories import PasswordResetTokenRepository
from modules.shared.auth.domain import PasswordRecoveryNotifier
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.application import PasswordRecovery
from modules.shared.auth.infrastructure.repositories import PostgresUserRepository
from modules.shared.auth.infrastructure.repositories import RedisPasswordResetTokenRepository
from modules.shared.auth.infrastructure import EmailPasswordRecoveryNotifier
from modules.shared.environ.infrastructure import PyEnviron


class PasswordRecoveryController:
    def __init__(
        self,
        session: AsyncSession,
        user_repository: UserRepository | None = None,
        password_reset_token_repository: PasswordResetTokenRepository | None = None,
        password_recovery_notifier: PasswordRecoveryNotifier | None = None,
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
        self.__password_recovery_notifier = password_recovery_notifier or EmailPasswordRecoveryNotifier(
            email_client=smtplib.SMTP("smtp.gmail.com", 587),
            environ=self.__environ,
        )

    async def recover(self, body: dict):
        try:
            password_recovery = PasswordRecovery(
                user_repository=self.__user_repository,
                password_reset_token_repository=self.__password_reset_token_repository,
                password_recovery_notifier=self.__password_recovery_notifier,
                environ=self.__environ,
            )

            await password_recovery.recover(email=body.get("email"))

            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK

        except UserDoesNotExist as ex:
            response = {
                "success": True,
                "message": messages.SUCCESS_MESSAGE,
                "data": {}
            }, status.HTTP_200_OK
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
