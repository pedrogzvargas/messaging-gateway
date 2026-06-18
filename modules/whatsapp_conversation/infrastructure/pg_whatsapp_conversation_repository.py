from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from modules.whatsapp_conversation.domain import WhatsappConversationRepository
from sqlalchemy_models import WhatsappConversationModel
from .conversation_mapper import ConversationMapper


class PgWhatsappConversationRepository(WhatsappConversationRepository):
    """
    PgWhatsappConversationRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, customer):
        """add wa conversation to session"""

        self.__session.add(ConversationMapper.to_model(customer))
        await self.__session.flush()

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for conversation"""

        stmt = select(WhatsappConversationModel).order_by(desc(WhatsappConversationModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(WhatsappConversationModel, field):
                column = getattr(WhatsappConversationModel, field)

                if isinstance(column.type, String) and isinstance(value, str):
                    stmt = stmt.where(column.ilike(value))
                else:
                    stmt = stmt.where(column == value)

        # count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.__session.scalar(count_stmt)

        # pagination
        limit = total if list_all else limit
        pages = (total + limit - 1) // limit if total >= 1 else 0

        if total > limit:
            offset = (page - 1) * limit
            stmt = stmt.offset(offset).limit(limit)

        result = await self.__session.execute(stmt)
        results = result.scalars().all()

        results = [ConversationMapper.to_domain(result) for result in results]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "results": results,
        }

    def all(self):
        """list all conversations"""

        result = self.__session.query(WhatsappConversationModel).all()
        return result

    async def get(self, id: UUID):
        """get conversation"""

        customer = await self.__session.get(WhatsappConversationModel, id)

        if customer:
            return ConversationMapper.to_domain(customer)

        return None

    async def get_by_phone(self, phone: str):
        """get conversation"""

        stmt = select(WhatsappConversationModel).where(WhatsappConversationModel.phone_number == phone)
        query_result = await self.__session.execute(stmt)
        conversation = query_result.scalar_one_or_none()

        if conversation is None:
            return None

        return ConversationMapper.to_domain(conversation)

    async def delete(self, id: UUID):
        """delete conversation"""

        customer = await self.__session.get(WhatsappConversationModel, id)

        if customer:
            await self.__session.delete(customer)
            await self.__session.flush()
