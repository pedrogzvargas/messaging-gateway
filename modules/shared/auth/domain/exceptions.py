class UserDoesNotExist(Exception):
    ...


class LockedAccount(Exception):
    ...


class WrongCredentials(Exception):
    ...


class ExpiredTokenError(Exception):
    ...


class InvalidTokenError(Exception):
    ...
