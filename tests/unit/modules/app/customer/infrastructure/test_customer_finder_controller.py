from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.customer.infrastructure import CustomerFinderController
from modules.app.customer.domain import Customer


@pytest.mark.asyncio
async def test_customer_finder() -> None:
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    customer_repository = AsyncMock()
    customer_repository.get.return_value = Customer(
        id=UUID(customer_id),
        name="Pedro",
        last_name="Gonzalez",
        second_last_name="Vargas",
    )

    customer_finder_controller = CustomerFinderController(
        session=session,
        customer_repository=customer_repository,
    )

    response, code = await customer_finder_controller.find(customer_id=UUID(customer_id))

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").id == UUID(customer_id)


@pytest.mark.asyncio
async def test_customer_does_not_exist_on_customer_finder() -> None:
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    customer_repository = AsyncMock()
    customer_repository.get.return_value = None

    customer_finder_controller = CustomerFinderController(
        session=session,
        customer_repository=customer_repository,
    )

    response, code = await customer_finder_controller.find(customer_id=UUID(customer_id))

    assert response.get("success") is False
    assert code == 404
