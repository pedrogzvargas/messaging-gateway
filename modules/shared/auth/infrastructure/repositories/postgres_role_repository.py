from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy_models import RoleModel
from modules.shared.auth.domain.repositories import RoleRepository
from modules.shared.auth.infrastructure.mappers import RoleMapper


class PostgresRoleRepository(RoleRepository):
    """
    PostgresRoleRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def list_by_ids(self, ids: List):
        """list roles by ids"""

        stmt = select(RoleModel).where(RoleModel.id.in_(ids))
        query_result = await self.__session.execute(stmt)
        results = query_result.scalars().all()

        results = [RoleMapper.to_domain(result) for result in results]

        return results
