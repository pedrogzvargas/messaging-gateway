from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_models import SessionModel
from modules.shared.auth.domain.repositories import SessionRepository
from modules.shared.auth.infrastructure.mappers import SessionMapper


class PostgresSessionRepository(SessionRepository):
    """
    PostgresSessionRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, session):
        """add session to db session"""
        self.__session.add(SessionMapper.to_model(session))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get session"""

        session = await self.__session.get(SessionModel, id)

        if session:
            return SessionMapper.to_domain(session)

        return session

    async def patch(self, session):
        """patch refresh token method"""

        await self.__session.merge(SessionMapper.to_model(session))
