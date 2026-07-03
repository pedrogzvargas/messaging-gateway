import uuid
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.password_hasher.domain import PasswordHasher
from modules.shared.auth.domain.entities import RefreshToken
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain import AuthAttemptHandler
from modules.shared.auth.domain.repositories import UserRepository
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.domain.repositories import UserRoleRepository
from modules.shared.auth.domain.repositories import RoleRepository
from modules.shared.auth.domain.repositories import PermissionRepository
from modules.shared.auth.domain.repositories import RolePermissionRepository
from modules.shared.auth.domain import UserDoesNotExist
from modules.shared.auth.domain import WrongCredentials
from modules.shared.auth.domain import LockedAccount


class Login:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        user_repository: UserRepository,
        user_role_repository: UserRoleRepository,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
        refresh_token_repository: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        token_handler: TokenHandler,
        auth_attempt_handler: AuthAttemptHandler,
    ):

        self.__user_repository = user_repository
        self.__user_role_repository = user_role_repository
        self.__role_repository = role_repository
        self.__permission_repository = permission_repository
        self.__role_permission_repository = role_permission_repository
        self.__refresh_token_repository = refresh_token_repository
        self.__unit_of_work = unit_of_work
        self.__password_hasher = password_hasher
        self.__token_handler = token_handler
        self.__auth_attempt_handler = auth_attempt_handler

    async def login(self, email: str, password: str):
        if await self.__auth_attempt_handler.is_blocked(email=email):
            raise LockedAccount(f"Account with username: {email} locked")

        user = await self.__user_repository.get_by_email(email=email)

        if not user:
            await self.__auth_attempt_handler.register_failed_attempt(email=email)
            raise UserDoesNotExist(f"User with username: {email} does not exist")

        if not self.__password_hasher.verify(hashed_password=user.password, password=password):
            await self.__auth_attempt_handler.register_failed_attempt(email=email)
            raise WrongCredentials(f"Wrong credentials")

        await self.__auth_attempt_handler.clear_attempts(email=email)

        users_roles = await self.__user_role_repository.list_by_user_id(user_id=user.id)
        user_role_ids = [users_role.role_id for users_role in users_roles]

        roles = await self.__role_repository.list_by_ids(user_role_ids)
        role_permissions = await self.__role_permission_repository.list_by_role_ids(user_role_ids)

        permission_ids = [permission.permission_id for permission in role_permissions]
        permissions = await self.__permission_repository.list_by_ids(permission_ids)

        jti = uuid.uuid4()

        access_token_payload = dict(
            sub=str(user.id),
            type="access",
            roles=[role.name for role in roles],
            permissions=[permission.name for permission in permissions],
            jti=str(jti),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=15),
        )

        refresh_token_payload = dict(
            sub=str(user.id),
            type="refresh",
            jti=str(jti),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(hours=24),
        )

        access_token = self.__token_handler.encode(payload=access_token_payload)
        refresh_token = self.__token_handler.encode(payload=refresh_token_payload)
        refresh_token_entity = RefreshToken.create(id=jti, user_id=user.id, jti=jti)

        async with self.__unit_of_work:
            await self.__refresh_token_repository.add(refresh_token=refresh_token_entity)

        return access_token, refresh_token
