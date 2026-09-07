class UserDoesNotExist(Exception):
    ...


class TemporarilyLocketAccount(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after

        super().__init__("Login is temporarily locked.")


class WrongCredentials(Exception):
    ...


class ExpiredTokenError(Exception):
    ...


class InvalidTokenError(Exception):
    ...
