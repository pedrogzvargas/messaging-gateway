from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_models import RefreshTokenModel
from modules.shared.auth.domain.repositories import RefreshTokenRepository
from modules.shared.auth.infrastructure.mappers import RefreshTokenMapper


class PostgresRefreshTokenRepository(RefreshTokenRepository):
    """
    PostgresRefreshTokenRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, refresh_token):
        """add refresh token to session"""
        self.__session.add(RefreshTokenMapper.to_model(refresh_token))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get refresh token"""

        refresh_token = await self.__session.get(RefreshTokenModel, id)

        if refresh_token:
            return RefreshTokenMapper.to_domain(refresh_token)

        return refresh_token

    async def patch(self, refresh_token):
        """patch refresh token method"""

        await self.__session.merge(RefreshTokenMapper.to_model(refresh_token))
