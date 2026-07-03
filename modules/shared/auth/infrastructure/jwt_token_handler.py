from jwt import encode
from jwt import decode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain.exceptions import ExpiredTokenError
from modules.shared.auth.domain.exceptions import InvalidTokenError as DomainInvalidTokenError


class JwtTokenHandler(TokenHandler):

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.__secret_key = secret_key
        self.__algorithm = algorithm

    def encode(self, payload):
        return encode(key=self.__secret_key, payload=payload, algorithm=self.__algorithm)

    def decode(self, token):
        try:
            return decode(jwt=token, key=self.__secret_key, algorithms=self.__algorithm)

        except ExpiredSignatureError as e:
            raise ExpiredTokenError("Expired token error") from e

        except InvalidTokenError as e:
            raise DomainInvalidTokenError("Invalid token error") from e
