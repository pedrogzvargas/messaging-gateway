from uuid import UUID
from modules.app.customer.domain import Customer
from modules.app.customer.domain import CustomerRepository
from modules.app.customer.domain.exceptions import CustomerDoesNotExist


class CustomerFinder:

    def __init__(self, customer_repository: CustomerRepository):
        self.__customer_repository = customer_repository

    async def find(self, customer_id: UUID) -> Customer:
        customer = await self.__customer_repository.get(customer_id)

        if not customer:
            raise CustomerDoesNotExist(f"Customer with id: {customer_id} not found")

        return customer
