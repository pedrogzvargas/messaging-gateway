from uuid import UUID
from modules.app.customer.domain import Customer
from modules.app.customer.domain import CustomerRepository
from modules.app.customer.domain.exceptions import CustomerDoesNotExist
from modules.shared.persistence.domain import UnitOfWork


class CustomerPatcher:

    def __init__(self, unit_of_work: UnitOfWork, customer_repository: CustomerRepository):
        self.__unit_of_work = unit_of_work
        self.__customer_repository = customer_repository

    async def patch(self, customer_id: UUID, data: dict) -> Customer:
        customer = await self.__customer_repository.get(customer_id)

        if not customer:
            raise CustomerDoesNotExist(f"Customer with id: {customer_id} not found")

        customer.patch(data=data)

        async with self.__unit_of_work:
            await self.__customer_repository.patch(customer)

        return customer
