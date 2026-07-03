from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy_models import PermissionModel
from modules.shared.auth.domain.repositories import PermissionRepository
from modules.shared.auth.infrastructure.mappers import PermissionMapper


class PostgresPermissionRepository(PermissionRepository):
    """
    PostgresPermissionRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def list_by_ids(self, ids: List):
        """list roles by ids"""

        stmt = select(PermissionModel).where(PermissionModel.id.in_(ids))
        query_result = await self.__session.execute(stmt)
        results = query_result.scalars().all()

        results = [PermissionMapper.to_domain(result) for result in results]

        return results
