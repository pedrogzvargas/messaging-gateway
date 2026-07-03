from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.auth.domain.repositories import UserRepository
from sqlalchemy import select
from sqlalchemy_models import UserModel
from modules.shared.auth.infrastructure.mappers import UserMapper


class PostgresUserRepository(UserRepository):
    """
    PostgresUserRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, user):
        """add user to session"""
        self.__session.add(UserMapper.to_model(user))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get user"""

        user = await self.__session.get(UserModel, id)

        if user:
            return UserMapper.to_domain(user)

        return user

    async def get_by_email(self, email: str):
        """get user"""

        stmt = select(UserModel).filter_by(email=email)

        user = (await self.__session.execute(stmt)).scalars().one_or_none()

        if user:
            return UserMapper.to_domain(user)

        return user

    async def patch(self, user):
        """patch user"""

        await self.__session.merge(UserMapper.to_model(user))
