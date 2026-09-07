from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.app.business.domain import BusinessRepository
from sqlalchemy_models import BusinessModel
from .business_mapper import BusinessMapper


class PgBusinessRepository(BusinessRepository):

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, id: UUID):
        """get business by id"""

        business = await self.__session.get(BusinessModel, id)

        if business is None:
            return None

        return BusinessMapper.to_domain(business)

    async def get_by_customer_id(self, customer_id: UUID):
        """get business by customer id"""

        stmt = select(BusinessModel).where(BusinessModel.customer_id == customer_id)
        query_result = await self.__session.execute(stmt)
        business = query_result.scalar_one_or_none()

        if business is None:
            return None

        return BusinessMapper.to_domain(business)
