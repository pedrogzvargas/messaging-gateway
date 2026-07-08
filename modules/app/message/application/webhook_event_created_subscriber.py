from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.conversation.domain import Conversation
from modules.app.contact.domain import Contact
from modules.app.message.domain import Message
from modules.shared.persistence.domain import UnitOfWork
from modules.shared.environ.domain import Environ
from modules.shared.bus.event.domain import EventBus
from modules.app.conversation.domain import ConversationRepository
from modules.app.message.domain import MessageRepository
from modules.app.channel_account.domain import ChannelAccountRepository
from modules.app.contact.domain import ContactRepository
from modules.shared.bus.event.application import subscriber
from modules.shared.persistence.infrastructure import AlchemyUnitOfWork
from modules.app.conversation.infrastructure import PgConversationRepository
from modules.app.message.infrastructure import PgMessageRepository
from modules.app.channel_account.infrastructure import PgChannelAccountRepository
from modules.app.contact.infrastructure import PgContactRepository
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.bus.event.infrastructure import RedisEventBus
from redis.asyncio import Redis


@subscriber("app.webhook_event.created")
class WebhookEventCreatedSubscriber:

    def __init__(
        self,
        session: AsyncSession | None = None,
        event_bus: EventBus | None = None,
        environ: Environ | None = None,
        unit_of_work: UnitOfWork | None = None,
        conversation_repository: ConversationRepository | None = None,
        channel_account_repository: ChannelAccountRepository | None = None,
        contact_repository: ContactRepository | None = None,
        message_repository: MessageRepository | None = None,
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
        self.__conversation_repository = conversation_repository or PgConversationRepository(session=self.__session)
        self.__channel_account_repository = channel_account_repository or PgChannelAccountRepository(session=self.__session)
        self.__contact_repository = contact_repository or PgContactRepository(session=self.__session)
        self.__message_repository = message_repository or PgMessageRepository(session=self.__session)

    async def handle(self, event):
        provider_id = event.get("provider_id")
        message_body = event.get("payload", {})
        entry = message_body.get("entry", [])
        changes = entry[0].get("changes", [])
        value = changes[0].get("value")
        messages = value.get("messages", [])
        contacts = value.get("contacts", [])

        if not messages:
            return

        message = messages[0]
        message_contact = contacts[0]

        if message.get("type", "") != "text":
            return

        phone_number = message.get("from", "")
        text = message.get("text", {}).get("body", "")

        channel_account = await self.__channel_account_repository.get_by_provider_id(provider_id=provider_id)

        if not channel_account:
            await self.__session.close()
            return

        contact = await self.__contact_repository.get_by_provider_id(provider_id=phone_number)

        contact_id = contact.id if contact else uuid4()
        if not contact:
            contact = Contact.create(
                id=uuid4(),
                provider_id=phone_number,
                channel_account_id=channel_account.id,
                display_name=message_contact.get("profile", {}).get("name", ""),
            )
            await self.__contact_repository.add(contact)

        conversation = await self.__conversation_repository.get_by_fields(
            channel_account_id=channel_account.id,
            contact_id=contact_id,
        )
        conversation_id = conversation.id if conversation else uuid4()

        if not conversation:
            conversation = Conversation.create(
                id=conversation_id,
                channel_account_id=channel_account.id,
                contact_id=contact.id,
            )
            await self.__conversation_repository.add(conversation)

        message_id = uuid4()
        message_entity = Message.create(
            id=message_id,
            conversation_id=conversation_id,
            role="user", # assistant
            message_id=message.get("id", ""),
            message_type=message.get("type", ""),
            message=text,
            direction="inbound", # outbound
            timestamp=datetime.fromtimestamp(int(message.get("timestamp"))), # message.get("timestamp"),
            payload=message_body,
        )

        async with self.__unit_of_work:
            await self.__message_repository.add(message_entity)

        await self.__event_bus.publish(message_entity.pull_domain_events())

        await self.__session.close()
