from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import asc
from sqlalchemy import func
from sqlalchemy import select
from modules.whatsapp_message.domain import WhatsappMessageRepository
from sqlalchemy_models import WhatsappMessageModel
from .message_mapper import MessageMapper


class PgWhatsappMessageRepository(WhatsappMessageRepository):
    """
    PgWhatsappConversationRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, customer):
        """add wa conversation to session"""

        self.__session.add(MessageMapper.to_model(customer))
        await self.__session.flush()

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for conversation"""

        stmt = select(WhatsappMessageModel).order_by(desc(WhatsappMessageModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(WhatsappMessageModel, field):
                column = getattr(WhatsappMessageModel, field)

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

        results = [MessageMapper.to_domain(result) for result in results]

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "results": results,
        }

    def all(self):
        """list all conversations"""

        result = self.__session.query(WhatsappMessageModel).all()
        return result

    async def get(self, id: UUID):
        """get conversation"""

        customer = await self.__session.get(WhatsappMessageModel, id)

        if customer:
            return MessageMapper.to_domain(customer)

        return None

    async def get_by_phone(self, phone: str):
        """get conversation"""

        stmt = select(WhatsappMessageModel).where(WhatsappMessageModel.phone_number == phone)
        query_result = await self.__session.execute(stmt)
        conversation = query_result.scalar_one_or_none()

        if conversation is None:
            return None

        return MessageMapper.to_domain(conversation)

    async def list_by_conversation(self, conversation_id: str, limit: int = 10):
        """get conversation"""

        stmt = (select(
            WhatsappMessageModel
        ).where(
            WhatsappMessageModel.conversation_id == conversation_id
        ).order_by(
            desc(WhatsappMessageModel.timestamp)
        ).limit(limit))
        query_result = await self.__session.execute(stmt)
        messages = query_result.scalars().all()

        if messages is None:
            return None

        return [MessageMapper.to_domain(message) for message in messages]

    async def delete(self, id: UUID):
        """delete conversation"""

        customer = await self.__session.get(WhatsappMessageModel, id)

        if customer:
            await self.__session.delete(customer)
            await self.__session.flush()
