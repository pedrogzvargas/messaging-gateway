from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from modules.app.customer.domain import CustomerRepository
from sqlalchemy_models import CustomerModel
from .customer_mapper import CustomerMapper


class PgCustomerRepository(CustomerRepository):
    """
    PgCustomerRepository
    """

    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, id: UUID):
        """get customer"""

        customer = await self.__session.get(CustomerModel, id)

        if customer:
            return CustomerMapper.to_domain(customer)

        return None

    async def patch(self, customer):
        """patch customer"""

        model = await self.__session.get(CustomerModel, customer.id)
        model.name = customer.name
        model.last_name = customer.last_name
        model.second_last_name = customer.second_last_name
