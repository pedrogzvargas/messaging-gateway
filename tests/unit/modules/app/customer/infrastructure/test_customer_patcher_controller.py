from uuid import UUID
import pytest
from unittest.mock import AsyncMock
from modules.app.customer.infrastructure import CustomerPatcherController
from modules.app.customer.domain import Customer


@pytest.mark.asyncio
async def test_customer_patcher() -> None:
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    unit_of_work = AsyncMock()
    customer_repository = AsyncMock()
    customer_repository.get.return_value = Customer(
        id=UUID(customer_id),
        name="Pedro",
        last_name="Gonzalez",
        second_last_name="Vargas",
    )

    customer_patcher_controller = CustomerPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        customer_repository=customer_repository,
    )

    response, code = await customer_patcher_controller.patch(
        customer_id=UUID(customer_id),
        data={"name": "Pedro Antonio", "last_name": "Gonzalez", "second_last_name": "Vargas"},
    )

    assert response.get("success") is True
    assert code == 200
    assert response.get("data").name == "Pedro Antonio"
    customer_repository.patch.assert_awaited_once()


@pytest.mark.asyncio
async def test_customer_patcher_only_patches_whitelisted_fields() -> None:
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    unit_of_work = AsyncMock()
    customer_repository = AsyncMock()
    customer_repository.get.return_value = Customer(
        id=UUID(customer_id),
        name="Pedro",
        last_name="Gonzalez",
        second_last_name="Vargas",
    )

    customer_patcher_controller = CustomerPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        customer_repository=customer_repository,
    )

    other_id = "9b2f4c5d-6e7f-4a8b-9c1d-2e3f4a5b6c7d"
    response, code = await customer_patcher_controller.patch(
        customer_id=UUID(customer_id),
        data={"name": "Pedro Antonio", "id": other_id},
    )

    assert code == 200
    assert response.get("data").id == UUID(customer_id)
    assert response.get("data").name == "Pedro Antonio"


@pytest.mark.asyncio
async def test_customer_does_not_exist_on_customer_patcher() -> None:
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    session = AsyncMock()
    unit_of_work = AsyncMock()
    customer_repository = AsyncMock()
    customer_repository.get.return_value = None

    customer_patcher_controller = CustomerPatcherController(
        session=session,
        unit_of_work=unit_of_work,
        customer_repository=customer_repository,
    )

    response, code = await customer_patcher_controller.patch(
        customer_id=UUID(customer_id),
        data={"name": "Pedro Antonio"},
    )

    assert response.get("success") is False
    assert code == 404
    customer_repository.patch.assert_not_awaited()
