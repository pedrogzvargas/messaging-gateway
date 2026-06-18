from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession
from modules.chat.domain import LLM
from modules.chat.domain import Chat
from modules.chat.domain import MessageChannel
from modules.chat.domain import QuestionRepository
from modules.whatsapp_conversation.domain import WhatsappConversationRepository
from modules.shared.environ.domain import Environ
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.chat.infrastructure import OpenaiLLM
from modules.chat.infrastructure import LangGraphChat
from modules.chat.infrastructure import WhatsappMessageChannel
from modules.chat.infrastructure import PGVectorRepository
from modules.chat.infrastructure.graph import AIGraph
from modules.whatsapp_conversation.infrastructure import PgWhatsappConversationRepository


class ConversationController:
    """
    ConversationController
    """

    def __init__(
        self,
        session: AsyncSession,
        unit_of_work: UnitOfWork | None = None,
        llm: LLM | None = None,
        chat: Chat | None = None,
        message_channel: MessageChannel | None = None,
        question_repository: QuestionRepository | None = None,
        whatsapp_conversation_repository: WhatsappConversationRepository | None = None,
        environ: Environ | None = None,
    ):
        self.__session = session
        self.__environ = environ or PyEnviron()
        self.__llm = llm or OpenaiLLM(
            client=ChatOpenAI(
                model=self.__environ.get_str("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
                api_key=self.__environ.get_str("OPENAI_API_KEY"),
            )
        )
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__question_repository = question_repository or PGVectorRepository(
            session=self.__session,
            embeddings=OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=self.__environ.get_str("OPENAI_API_KEY"),
            )
        )
        self.__whatsapp_conversation_repository = whatsapp_conversation_repository or PgWhatsappConversationRepository(
            session=self.__session,
        )
        self.__chat = chat or LangGraphChat(
            graph=AIGraph(
                unit_of_work=self.__unit_of_work,
                question_repository=self.__question_repository,
                whatsapp_conversation_repository=self.__whatsapp_conversation_repository,
                llm=self.__llm
            ).build_graph()
        )
        self.__message_channel = message_channel or WhatsappMessageChannel(environ=self.__environ)

    async def message(self, payload):
        try:
            value = (
                payload["entry"][0]
                ["changes"][0]
                ["value"]
            )

            # Ignorar eventos de status
            if "messages" not in value:
                return {"status": "ignored"}

            message = value["messages"][0]

            if message["type"] != "text":
                return {"status": "unsupported"}

            phone = message["from"]
            text = message["text"]["body"]

            response = await self.__chat.process_message(user_id=phone, message=text)
            await self.__message_channel.send_message(identifier=phone, message=response.get("response"))

            return {"status": "success"}

        except Exception as e:
            return {"status": "error"}
