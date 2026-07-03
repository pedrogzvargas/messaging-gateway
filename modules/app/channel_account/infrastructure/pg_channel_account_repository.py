from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.app.channel_account.domain import ChannelAccountRepository
from sqlalchemy_models import ChannelAccountModel
from .channel_account_mapper import ChannelAccountMapper


class PgChannelAccountRepository(ChannelAccountRepository):
    """
    PgChannelAccountRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, id: UUID):
        """get channel account"""

        customer = await self.__session.get(ChannelAccountModel, id)

        if customer:
            return ChannelAccountMapper.to_domain(customer)

        return None

    async def get_by_provider_id(self, provider_id: str):
        """get channel account"""

        stmt = select(ChannelAccountModel).where(ChannelAccountModel.provider_id == provider_id)
        query_result = await self.__session.execute(stmt)
        channel_account = query_result.scalar_one_or_none()

        if channel_account is None:
            return None

        return ChannelAccountMapper.to_domain(channel_account)
