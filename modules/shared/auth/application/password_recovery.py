from secrets import token_urlsafe
from modules.shared.auth.domain import PasswordRecoveryNotifier
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.auth.domain.repositories import PasswordResetTokenRepository
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.environ.domain import Environ


class PasswordRecovery:
    def __init__(
        self,
        user_repository: UserRepository,
        password_reset_token_repository: PasswordResetTokenRepository,
        password_recovery_notifier: PasswordRecoveryNotifier,
        environ: Environ,
    ):
        self.__user_repository = user_repository
        self.__password_reset_token_repository = password_reset_token_repository
        self.__password_recovery_notifier = password_recovery_notifier
        self.__environ = environ

    async def recover(self, email: str):
        user = await self.__user_repository.get_by_email(email=email)

        if not user:
            raise UserDoesNotExist(f"User with email {email} does not exist")

        token = token_urlsafe(32)

        # self.__password_recovery_notifier.send_reset_link(user=user, token=token)
        await self.__password_reset_token_repository.save(
            token=token,
            user_id=user.id,
            expires_in=self.__environ.get_int("PASSWORD_RECOVERY_TIME_SECONDS", 300),
        )
