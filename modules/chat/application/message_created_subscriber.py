from uuid import uuid4
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.environ.domain import Environ
from modules.chat.domain import LLM
from modules.chat.domain import QuestionRepository
from modules.chat.domain import MessageChannel
from modules.whatsapp_message.domain import WhatsappMessage
from modules.whatsapp_message.domain import WhatsappMessageRepository
from modules.shared.bus.event.application import subscriber
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from modules.chat.infrastructure import OpenaiLLM
from modules.chat.infrastructure.graph import AIGraph
from modules.chat.infrastructure.state import ChatState
from modules.whatsapp_message.infrastructure import PgWhatsappMessageRepository
from modules.chat.infrastructure import PGVectorRepository
from modules.chat.infrastructure import WhatsappMessageChannel
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


@subscriber("app.whatsapp_message.created")
class MessageCreatedSubscriber:

    def __init__(
        self,
        session: AsyncSession | None = None,
        unit_of_work: UnitOfWork | None = None,
        environ: Environ | None = None,
        llm: LLM | None = None,
        whatsapp_message_repository: WhatsappMessageRepository | None = None,
        question_repository: QuestionRepository | None = None,
        message_channel: MessageChannel | None = None,
    ):
        self.__environ = environ or PyEnviron()
        self.__session = session or AsyncAlchemySessionCreator(
            dialect=self.__environ.get_str("POSTGRES_DIALECT"),
            driver=self.__environ.get_str("POSTGRES_DRIVER"),
            host=self.__environ.get_str("POSTGRES_HOST"),
            user=self.__environ.get_str("POSTGRES_USER"),
            password=self.__environ.get_str("POSTGRES_PASSWORD"),
            port=self.__environ.get_str("POSTGRES_PORT"),
            db=self.__environ.get_str("POSTGRES_DB"),
            echo=self.__environ.get_bool("SQL_ECHO", False),
        ).get_session()
        self.__unit_of_work = unit_of_work or AlchemyUnitOfWork(session=self.__session)
        self.__llm = llm or OpenaiLLM(
            client=ChatOpenAI(
                model=self.__environ.get_str("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
                api_key=self.__environ.get_str("OPENAI_API_KEY"),
            )
        )
        self.__whatsapp_message_repository = whatsapp_message_repository or PgWhatsappMessageRepository(session=self.__session)
        self.__question_repository = question_repository or PGVectorRepository(
            session=self.__session,
            embeddings=OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=self.__environ.get_str("OPENAI_API_KEY"),
            )
        )
        self.__message_channel = message_channel or WhatsappMessageChannel(environ=self.__environ)

    async def handle(self, event):
        print("MessageCreatedSubscriber", event)

        graph = AIGraph(
            whatsapp_message_repository=self.__whatsapp_message_repository,
            question_repository=self.__question_repository,
            llm=self.__llm,
        ).build_graph()

        message = event.get("message_text")
        phone_number = event.get("from_number")
        initial_state = ChatState()
        initial_state.message = f"{message}"
        initial_state.phone_number = phone_number
        initial_state.conversation_id = event.get("conversation_id")
        result = await graph.ainvoke(initial_state)
        print(result)

        sent_message_response = await self.__message_channel.send_message(
            identifier=phone_number,
            message=result.get("response"),
        )
        sent_message = sent_message_response.get("messages")[0]

        whatsapp_message = WhatsappMessage(
            id=uuid4(),
            conversation_id=event.get("conversation_id"),
            role="assistant",
            wa_message_id=sent_message.get("id"),
            from_number=self.__environ.get_str("WA_PHONE_NUMBER_ID"),
            to_number=phone_number,
            message_type="text",
            message_text=result.get("response"),
            direction="outbound",
            timestamp=datetime.now(),
            raw_payload=sent_message_response
        )
        print(sent_message)

        async with self.__unit_of_work:
            await self.__whatsapp_message_repository.add(whatsapp_message)

        await self.__session.close()
