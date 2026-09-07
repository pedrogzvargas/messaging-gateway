from uuid import UUID
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import WrongCredentials


class PasswordChange:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self.__unit_of_work = unit_of_work
        self.__user_repository = user_repository
        self.__password_hasher = password_hasher

    async def change(self, user_id: UUID, password: str, new_password: str):

        user = await self.__user_repository.get(id=user_id)

        if not user:
            raise UserDoesNotExist(f"User with id {user_id} does not exist")

        if not self.__password_hasher.verify(hashed_password=user.password, password=password):
            raise WrongCredentials("Wrong password")

        user.password = self.__password_hasher.hash(new_password)

        async with self.__unit_of_work:
            await self.__user_repository.patch(user)
