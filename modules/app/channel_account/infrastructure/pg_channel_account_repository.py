from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import desc
from sqlalchemy import func
from modules.app.channel_account.domain import ChannelAccountRepository
from sqlalchemy_models import ChannelAccountModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import BusinessModel
from modules.shared.http.infrastructure import PageResult
from modules.app.channel_account.application import ChannelAccountItem
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

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[ChannelAccountItem]:
        """simple search for conversation"""

        allowed_filters = {
            "channel": (ChannelModel.name, "contains"),
            "business": (BusinessModel.name, "contains"),
            "provider_id": (ChannelAccountModel.provider_id, "contains"),
        }

        stmt = select(
            ChannelAccountModel.id,
            ChannelModel.name.label("channel"),
            BusinessModel.name.label("business"),
            ChannelAccountModel.provider_id,
            ChannelAccountModel.created_at,
            ChannelAccountModel.updated_at,
        ).join(
            ChannelAccountModel, ChannelModel.id == ChannelAccountModel.channel_id
        ).join(
            BusinessModel, ChannelAccountModel.business_id == BusinessModel.id
        ).order_by(desc(ChannelAccountModel.created_at))

        # filters
        for field, value in filters.items():
            column, operator = allowed_filters.get(field, (None, None))
            if column:
                match operator:
                    case "contains":
                        stmt = stmt.where(column.ilike(f"%{value}%"))
                    case "eq":
                        stmt = stmt.where(column == value)
                    case "gte":
                        stmt = stmt.where(column >= value)

        # count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.__session.scalar(count_stmt)

        # pagination
        pages = (total + limit - 1) // limit if total >= 1 else 0

        if total > limit:
            offset = (page - 1) * limit
            stmt = stmt.offset(offset).limit(limit)

        result = await self.__session.execute(stmt)
        results = result.mappings().all()

        return PageResult[ChannelAccountItem](
            page=page,
            limit=limit,
            total=total,
            pages=pages,
            items=results,
        )
