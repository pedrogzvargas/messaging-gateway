from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from modules.whatsapp_conversation.domain import WhatsappConversation
from modules.whatsapp_message.domain import WhatsappMessage
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.whatsapp_conversation.domain import WhatsappConversationRepository
from modules.whatsapp_message.domain import WhatsappMessageRepository
from modules.shared.bus.event.application import subscriber
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.whatsapp_conversation.infrastructure import PgWhatsappConversationRepository
from modules.whatsapp_message.infrastructure import PgWhatsappMessageRepository
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure import RedisEventBus
from redis.asyncio import Redis


@subscriber("app.whatsapp_webhook.created")
class WhatsappWebhookCreatedSubscriber:

    def __init__(
        self,
        session: AsyncSession | None = None,
        event_bus: EventBus | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
        whatsapp_conversation_repository: WhatsappConversationRepository | None = None,
        whatsapp_message_repository: WhatsappMessageRepository | None = None,
    ):
        self.__environ = environ or PyEnviron()
        self.__event_bus = event_bus or RedisEventBus(
            redis_client=Redis(
                host=self.__environ.get_str("REDIS_HOST"),
                port=self.__environ.get_str("REDIS_PORT"),
                decode_responses=True
            )
        )
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
        self.__whatsapp_conversation_repository = whatsapp_conversation_repository  or PgWhatsappConversationRepository(session=self.__session)
        self.__whatsapp_message_repository = whatsapp_message_repository or PgWhatsappMessageRepository(session=self.__session)

    async def handle(self, event):
        print("WhatsappWebhookCreatedSubscriber", event)

        whatsapp_message = event.get("payload", {})
        entry = whatsapp_message.get("entry", [])
        changes = entry[0].get("changes", [])
        value = changes[0].get("value")
        messages = value.get("messages", [])

        if not messages:
            return

        message = messages[0]

        if message.get("type", "") != "text":
            return

        phone_number = message.get("from", "")
        text = message.get("text", {}).get("body", "")

        conversation = await self.__whatsapp_conversation_repository.get_by_phone(phone=phone_number)
        conversation_id = conversation.id if conversation else uuid4()

        if not conversation:
            conversation = WhatsappConversation.create(
                id=conversation_id,
                phone_number=phone_number,
            )
            await self.__whatsapp_conversation_repository.add(conversation)

        message_id = uuid4()
        whatsapp_message = WhatsappMessage.create(
            id=message_id,
            conversation_id=conversation_id,
            role="user", # assistant
            wa_message_id=message.get("id", ""),
            from_number=message.get("from", ""),
            to_number=value.get("metadata", {}).get("display_phone_number", ""),
            message_type=message.get("type", ""),
            message_text=text,
            direction="inbound", # outbound
            timestamp=datetime.fromtimestamp(int(message.get("timestamp"))), # message.get("timestamp"),
            raw_payload=whatsapp_message,
        )

        async with self.__unit_of_work:
            await self.__whatsapp_message_repository.add(whatsapp_message)

        await self.__event_bus.publish(whatsapp_message.pull_domain_events())

        await self.__session.close()
