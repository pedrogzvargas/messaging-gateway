from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import String
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import select
from modules.app.message.domain import MessageRepository
from sqlalchemy_models import MessageModel
from .message_mapper import MessageMapper


class PgMessageRepository(MessageRepository):
    """
    PgMessageRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, customer):
        """add wa conversation to session"""

        self.__session.add(MessageMapper.to_model(customer))
        await self.__session.flush()

    async def simple_search(self, filters: dict, limit: int = 10, page: int = 1, list_all: bool = False):
        """simple search for conversation"""

        stmt = select(MessageModel).order_by(desc(MessageModel.created_at))

        # filters
        for field, value in filters.items():
            if hasattr(MessageModel, field):
                column = getattr(MessageModel, field)

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

        result = self.__session.query(MessageModel).all()
        return result

    async def get(self, id: UUID):
        """get conversation"""

        customer = await self.__session.get(MessageModel, id)

        if customer:
            return MessageMapper.to_domain(customer)

        return None

    async def get_by_phone(self, phone: str):
        """get conversation"""

        stmt = select(MessageModel).where(MessageModel.phone_number == phone)
        query_result = await self.__session.execute(stmt)
        conversation = query_result.scalar_one_or_none()

        if conversation is None:
            return None

        return MessageMapper.to_domain(conversation)

    async def list_by_conversation(self, conversation_id: str, limit: int = 10):
        """get conversation"""

        stmt = (select(
            MessageModel
        ).where(
            MessageModel.conversation_id == conversation_id
        ).order_by(
            desc(MessageModel.timestamp)
        ).limit(limit))
        query_result = await self.__session.execute(stmt)
        messages = query_result.scalars().all()

        if messages is None:
            return None

        return [MessageMapper.to_domain(message) for message in messages]

    async def delete(self, id: UUID):
        """delete conversation"""

        customer = await self.__session.get(MessageModel, id)

        if customer:
            await self.__session.delete(customer)
            await self.__session.flush()
