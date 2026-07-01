from uuid import uuid4
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from sqlalchemy.ext.asyncio import AsyncSession
from modules.shared.environ.domain import Environ
from modules.app.llm.domain import LLM
from modules.app.faq.domain import FaqRepository
from modules.app.message_channel.domain import MessageChannel
from modules.app.message.domain import Message
from modules.app.message.domain import MessageRepository
from modules.shared.bus.event.application import subscriber
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from modules.app.llm.infrastructure import OpenaiLLM
from modules.app.agent.infrastructure import BusinessGraph
from modules.app.agent.infrastructure.state import ChatState
from modules.app.message.infrastructure import PgMessageRepository
from modules.app.faq.infrastructure import PgFaqRepository
from modules.app.message_channel.infrastructure import WhatsappMessageChannel
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork


@subscriber("app.message.created")
class MessageCreatedSubscriber:

    def __init__(
        self,
        session: AsyncSession | None = None,
        unit_of_work: UnitOfWork | None = None,
        environ: Environ | None = None,
        llm: LLM | None = None,
        message_repository: MessageRepository | None = None,
        faq_repository: FaqRepository | None = None,
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
        self.__message_repository = message_repository or PgMessageRepository(session=self.__session)
        self.__faq_repository = faq_repository or PgFaqRepository(
            session=self.__session,
            embeddings=OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=self.__environ.get_str("OPENAI_API_KEY"),
            )
        )
        self.__message_channel = message_channel or WhatsappMessageChannel(environ=self.__environ)

    async def handle(self, event):

        graph = BusinessGraph(
            message_repository=self.__message_repository,
            faq_repository=self.__faq_repository,
            llm=self.__llm,
        ).build_graph()

        message = event.get("message_text")
        phone_number = event.get("from_number")
        initial_state = ChatState()
        initial_state.message = f"{message}"
        initial_state.phone_number = phone_number
        initial_state.conversation_id = event.get("conversation_id")
        result = await graph.ainvoke(initial_state)

        sent_message_response = await self.__message_channel.send_message(
            identifier=phone_number,
            message=result.get("response"),
        )
        sent_message = sent_message_response.get("messages")[0]

        message = Message(
            id=uuid4(),
            conversation_id=event.get("conversation_id"),
            role="assistant",
            message_id=sent_message.get("id"),
            message_type="text",
            message=result.get("response"),
            direction="outbound",
            timestamp=datetime.now(),
            payload=sent_message_response
        )

        async with self.__unit_of_work:
            await self.__message_repository.add(message)

        await self.__session.close()
