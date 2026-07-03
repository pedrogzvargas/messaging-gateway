from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy_models import UserRoleModel
from modules.shared.auth.domain.repositories import UserRoleRepository
from modules.shared.auth.infrastructure.mappers import UserRoleMapper


class PostgresUserRoleRepository(UserRoleRepository):
    """
    PostgresUserRoleRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def list_by_user_id(self, user_id: UUID):
        """get user roles by user_id"""

        stmt = select(UserRoleModel).where(UserRoleModel.user_id == user_id)
        query_result = await self.__session.execute(stmt)
        results = query_result.scalars().all()

        results = [UserRoleMapper.to_domain(result) for result in results]

        return results
