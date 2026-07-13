from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import desc
from modules.app.contact.domain import ContactRepository
from sqlalchemy_models import ContactModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import ChannelAccountModel
from modules.shared.http.infrastructure import PageResult
from modules.app.contact.application import ContactItem
from .contact_mapper import ContactMapper


class PgContactRepository(ContactRepository):
    """
    PgContactRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, contact):
        """add contact to session"""

        self.__session.add(ContactMapper.to_model(contact))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get contact"""

        customer = await self.__session.get(ContactModel, id)

        if customer:
            return ContactMapper.to_domain(customer)

        return None

    async def get_by_provider_id(self, provider_id: str):
        """get contact"""

        stmt = select(ContactModel).where(ContactModel.provider_id == provider_id)
        query_result = await self.__session.execute(stmt)
        contact = query_result.scalar_one_or_none()

        if contact is None:
            return None

        return ContactMapper.to_domain(contact)

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[ContactItem]:
        """simple search for contact"""

        allowed_filters = {
            "channel": (ChannelModel.name, "contains"),
            "display_name": (ContactModel.display_name, "contains"),
        }

        stmt = select(
            ContactModel.id,
            ChannelModel.name.label("channel"),
            ContactModel.provider_id,
            ContactModel.display_name,
            ContactModel.created_at,
            ContactModel.updated_at,
        ).join(
            ChannelAccountModel, ContactModel.channel_account_id == ChannelAccountModel.id
        ).join(
            ChannelModel, ChannelAccountModel.channel_id == ChannelModel.id
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

        return PageResult[ContactItem](
            page=page,
            limit=limit,
            total=total,
            pages=pages,
            items=results,
        )
