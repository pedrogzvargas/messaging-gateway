from uuid import uuid4
from uuid import UUID
from datetime import datetime
from datetime import timezone
from datetime import timedelta
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.domain.repositories import UserRoleRepository
from modules.shared.auth.domain.repositories import RoleRepository
from modules.shared.auth.domain.repositories import PermissionRepository
from modules.shared.auth.domain.repositories import RolePermissionRepository
from modules.shared.auth.domain import TokenHandler
from modules.shared.auth.domain.exceptions import InvalidTokenError
from modules.shared.auth.domain.entities import RefreshToken


class TokenRefresher:

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        refresh_token_repository: RefreshTokenRepository,
        user_role_repository: UserRoleRepository,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
        role_permission_repository: RolePermissionRepository,
        token_handler: TokenHandler,
        access_token_exp: int,
        refresh_token_exp: int,
    ):

        self.__refresh_token_repository = refresh_token_repository
        self.__user_role_repository = user_role_repository
        self.__role_repository = role_repository
        self.__permission_repository = permission_repository
        self.__role_permission_repository = role_permission_repository
        self.__token_handler = token_handler
        self.__unit_of_work = unit_of_work
        self.__access_token_exp = access_token_exp
        self.__refresh_token_exp = refresh_token_exp

    async def refresh(self, token):
        refresh_token_payload = self.__token_handler.decode(token)
        user_id = refresh_token_payload.get("sub")
        token_type = refresh_token_payload.get("type")
        current_jti = refresh_token_payload.get("jti")
        session_id = refresh_token_payload.get("session_id")

        if token_type != "refresh":
            raise InvalidTokenError("Invalid token")

        users_roles = await self.__user_role_repository.list_by_user_id(user_id=user_id)
        user_role_ids = [users_role.role_id for users_role in users_roles]

        roles = await self.__role_repository.list_by_ids(user_role_ids)
        role_permissions = await self.__role_permission_repository.list_by_role_ids(user_role_ids)

        permission_ids = [permission.permission_id for permission in role_permissions]
        permissions = await self.__permission_repository.list_by_ids(permission_ids)

        jti = uuid4()

        access_token_payload = dict(
            sub=str(user_id),
            type="access",
            roles=[role.name for role in roles],
            permissions=[permission.name for permission in permissions],
            jti=str(jti),
            session_id=str(session_id),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=self.__access_token_exp),
        )

        refresh_token_payload = dict(
            sub=str(user_id),
            type="refresh",
            jti=str(jti),
            session_id=str(session_id),
            iat=datetime.now(timezone.utc),
            exp=datetime.now(timezone.utc) + timedelta(minutes=self.__refresh_token_exp)
        )

        current_refresh_token = await self.__refresh_token_repository.get(id=current_jti)

        if current_refresh_token.revoked:
            raise InvalidTokenError("Refresh token revoked")

        current_refresh_token.patch({"revoked": True})

        access_token = self.__token_handler.encode(payload=access_token_payload)
        refresh_token = self.__token_handler.encode(payload=refresh_token_payload)
        refresh_token_entity = RefreshToken.create(id=jti, user_id=UUID(user_id), jti=jti, session_id=UUID(session_id))

        async with self.__unit_of_work:
            await self.__refresh_token_repository.patch(refresh_token=current_refresh_token)
            await self.__refresh_token_repository.add(refresh_token=refresh_token_entity)

        return access_token, refresh_token
