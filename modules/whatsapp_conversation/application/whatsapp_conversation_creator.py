from uuid import UUID
from modules.whatsapp_conversation.domain import WhatsappConversation
from modules.whatsapp_conversation.domain.exceptions import WhatsappConversationAlreadyExist
from modules.shared.persistence.domain import UnitOfWork
from modules.whatsapp_conversation.domain import WhatsappConversationRepository


class WhatsappConversationCreator:

    def __init__(self, unit_of_work: UnitOfWork, whatsapp_conversation_repository: WhatsappConversationRepository):
        self.__unit_of_work = unit_of_work
        self.__whatsapp_conversation_repository = whatsapp_conversation_repository

    async def create(self, id: UUID, phone_number: str):

        if await self.__whatsapp_conversation_repository.get(id=id):
            raise WhatsappConversationAlreadyExist(f" Conversation with id:{id} already exists")

        conversation = WhatsappConversation.create(
            id=id,
            phone_number=phone_number,
        )

        async with self.__unit_of_work:
            await self.__whatsapp_conversation_repository.add(conversation)
