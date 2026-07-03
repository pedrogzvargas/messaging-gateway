from uuid import UUID
from modules.app.conversation.domain import Conversation
from modules.app.conversation.domain.exceptions import ConversationAlreadyExist
from modules.shared.persistence.domain import UnitOfWork
from modules.app.conversation.domain import ConversationRepository


class ConversationCreator:

    def __init__(self, unit_of_work: UnitOfWork, conversation_repository: ConversationRepository):
        self.__unit_of_work = unit_of_work
        self.__conversation_repository = conversation_repository

    async def create(self, id: UUID, channel_account_id: UUID, contact_id: UUID,):

        if await self.__conversation_repository.get(id=id):
            raise ConversationAlreadyExist(f"Conversation with id:{id} already exists")

        conversation = Conversation.create(
            id=id,
            channel_account_id=channel_account_id,
            contact_id=contact_id,
        )

        async with self.__unit_of_work:
            await self.__conversation_repository.add(conversation)
