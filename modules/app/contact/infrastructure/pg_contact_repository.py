from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from modules.app.contact.domain import ContactRepository
from sqlalchemy_models import ContactModel
from .contact_mapper import ContactMapper


class PgContactRepository(ContactRepository):
    """
    PgContactRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add(self, contact):
        """add contact to session"""

        self.__session.add(ContactMapper.to_model(contact))
        await self.__session.flush()

    async def get(self, id: UUID):
        """get contact"""

        customer = await self.__session.get(ContactModel, id)

        if customer:
            return ContactMapper.to_domain(customer)

        return None

    async def get_by_provider_id(self, provider_id: str):
        """get contact"""

        stmt = select(ContactModel).where(ContactModel.provider_id == provider_id)
        query_result = await self.__session.execute(stmt)
        contact = query_result.scalar_one_or_none()

        if contact is None:
            return None

        return ContactMapper.to_domain(contact)
