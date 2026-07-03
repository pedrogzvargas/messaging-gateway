from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.auth.domain.repositories import PasswordResetTokenRepository
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import ExpiredTokenError


class PasswordReset:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        password_reset_token_repository: PasswordResetTokenRepository,
        password_hasher: PasswordHasher,
    ):
        self.__unit_of_work = unit_of_work
        self.__user_repository = user_repository
        self.__password_reset_token_repository = password_reset_token_repository
        self.__password_hasher = password_hasher

    async def reset(self, token: str, password: str):
        user_id = await self.__password_reset_token_repository.get_user_id(token=token)

        if not user_id:
            raise ExpiredTokenError(f'Token {token} expired')

        user = await self.__user_repository.get(id=user_id)

        if not user:
            raise UserDoesNotExist(f"User with id {user_id} does not exist")

        user.password = self.__password_hasher.hash(password)

        async with self.__unit_of_work:
            await self.__user_repository.patch(user)

        await self.__password_reset_token_repository.delete(token=token)
