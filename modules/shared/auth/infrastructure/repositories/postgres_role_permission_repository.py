from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy_models import RolePermissionModel
from modules.shared.auth.domain.repositories import RolePermissionRepository
from modules.shared.auth.infrastructure.mappers import RolePermissionMapper


class PostgresRolePermissionRepository(RolePermissionRepository):
    """
    PostgresRolePermissionRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def list_by_role_ids(self, ids: List):
        """list permissions by role ids"""

        stmt = select(RolePermissionModel).where(RolePermissionModel.role_id.in_(ids))
        query_result = await self.__session.execute(stmt)
        results = query_result.scalars().all()

        results = [RolePermissionMapper.to_domain(result) for result in results]

        return results
