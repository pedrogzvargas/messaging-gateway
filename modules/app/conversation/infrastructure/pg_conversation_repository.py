from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.app.conversation.domain import ConversationRepository
from sqlalchemy_models import ConversationModel
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

    async def get(self, id: UUID):
        """get conversation"""

        customer = await self.__session.get(ConversationModel, id)

        if customer:
            return ConversationMapper.to_domain(customer)

        return None

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
