from modules.shared.password_hasher.domain import PasswordHasher
from argon2 import PasswordHasher as Argon2Hasher
from argon2.exceptions import VerifyMismatchError


class Argon2PasswordHasher(PasswordHasher):
    def __init__(self, time_cost=3, memory_cost=2**16, parallelism=4):
        self.__hasher = Argon2Hasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
        )

    def hash(self, password):
        return self.__hasher.hash(password)

    def verify(self, hashed_password, password):
        try:
            return self.__hasher.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

    def needs_rehash(self, password):
        return self.__hasher.check_needs_rehash(password)
