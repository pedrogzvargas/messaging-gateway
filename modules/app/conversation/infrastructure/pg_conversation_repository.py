from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from modules.app.conversation.domain import ConversationRepository
from sqlalchemy_models import ConversationModel
from sqlalchemy_models import ChannelAccountModel
from sqlalchemy_models import ChannelModel
from sqlalchemy_models import ContactModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from modules.app.conversation.application import ConversationItem
from modules.shared.http.infrastructure import PageResult
from .conversation_mapper import ConversationMapper


class PgConversationRepository(ConversationRepository):
    """
    PgConversationRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, customer):
        """add wa conversation to session"""

        self.__session.add(ConversationMapper.to_model(customer))
        await self.__session.flush()

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1) -> PageResult[ConversationItem]:
        """simple search for conversation"""

        allowed_filters = {
            "channel": (ChannelModel.name, "contains"),
            "provider_id": (ContactModel.provider_id, "contains"),
            "name": (ContactModel.display_name, "contains"),
            "business_id": (ChannelAccountModel.business_id, "eq"),
        }

        stmt = select(
            ConversationModel.id,
            ChannelModel.name.label("channel"),
            ContactModel.provider_id,
            ContactModel.display_name,
            ConversationModel.created_at,
            ConversationModel.updated_at,
        ).join(
            ChannelAccountModel, ConversationModel.channel_account_id == ChannelAccountModel.id
        ).join(
            ContactModel, ConversationModel.contact_id == ContactModel.id
        ).join(
            ChannelModel, ChannelAccountModel.channel_id == ChannelModel.id
        ).order_by(desc(ConversationModel.created_at))

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

        return PageResult[ConversationItem](
            page=page,
            limit=limit,
            total=total,
            pages=pages,
            items=results,
        )

    async def get(self, id: UUID):
        """get conversation"""

        conversation = await self.__session.get(ConversationModel, id)

        if conversation:
            return ConversationMapper.to_domain(conversation)

        return None

    async def get_detail(self, id: UUID, business_id: UUID | None = None):
        """get conversation detail, optionally scoped to a business"""
        stmt = select(
            ConversationModel.id,
            ChannelModel.name.label("channel"),
            ContactModel.provider_id,
            ContactModel.display_name,
            ConversationModel.created_at,
            ConversationModel.updated_at,
        ).join(
            ChannelAccountModel, ConversationModel.channel_account_id == ChannelAccountModel.id
        ).join(
            ContactModel, ConversationModel.contact_id == ContactModel.id
        ).join(
            ChannelModel, ChannelAccountModel.channel_id == ChannelModel.id
        ).where(
            ConversationModel.id == id
        )

        if business_id is not None:
            stmt = stmt.where(ChannelAccountModel.business_id == business_id)

        query_result = await self.__session.execute(stmt)
        conversation = query_result.mappings().one_or_none()

        if conversation is None:
            return None

        return ConversationItem(**conversation)

    async def get_by_fields(self, **fields):
        """get conversation by fields"""

        stmt = select(ConversationModel)

        for field, value in fields.items():
            if hasattr(ConversationModel, field):
                column = getattr(ConversationModel, field)
                stmt = stmt.where(column == value)

        query_result = await self.__session.execute(stmt)
        conversation = query_result.scalar_one_or_none()

        if conversation is None:
            return None

        return ConversationMapper.to_domain(conversation)

    async def get_business_id_by_user_id(self, user_id: UUID): # TODO Fix when we has many business
        """get the business id owned by the given user"""

        stmt = select(BusinessModel.id).join(
            CustomerModel, BusinessModel.customer_id == CustomerModel.id
        ).where(
            CustomerModel.user_id == user_id
        )

        return await self.__session.scalar(stmt)

    async def get_business_id_by_conversation_id(self, conversation_id: UUID):
        """get the business id owned by the given user"""

        stmt = select(ChannelAccountModel.business_id).join(
            ConversationModel, ChannelAccountModel.id == ConversationModel.channel_account_id
        ).where(
            ConversationModel.id == conversation_id
        )

        return await self.__session.scalar(stmt)

    async def count_by_business_id(self, business_id: UUID, since: datetime | None = None) -> int:
        """count conversations owned by the given business, optionally created since a given datetime"""

        stmt = select(func.count(ConversationModel.id)).join(
            ChannelAccountModel, ConversationModel.channel_account_id == ChannelAccountModel.id
        ).where(
            ChannelAccountModel.business_id == business_id
        )

        if since is not None:
            stmt = stmt.where(ConversationModel.created_at >= since)

        return await self.__session.scalar(stmt) or 0
