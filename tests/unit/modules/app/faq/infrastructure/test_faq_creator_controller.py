from uuid import UUID
from types import SimpleNamespace
import pytest
from unittest.mock import AsyncMock
from modules.app.faq.infrastructure import FaqCreatorController
from modules.app.faq.domain import Faq
from modules.app.business.domain import Business


def _build_open_ai(embedding: list[float] | None = None):
    open_ai = AsyncMock()
    open_ai.embeddings.create.return_value = SimpleNamespace(
        data=[SimpleNamespace(embedding=embedding or [0.1] * 1536)]
    )
    return open_ai


@pytest.mark.asyncio
async def test_faq_creator() -> None:
    faq_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = "c75e8241-2de8-462d-b673-cfd55c0edc0f"

    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    faq_repository = AsyncMock()
    faq_repository.get.return_value = None
    business_repository = AsyncMock()
    business_repository.get_by_customer_id.return_value = Business(
        id=UUID(business_id),
        customer_id=UUID(customer_id),
        name="Vualdex",
    )
    open_ai = _build_open_ai()

    faq_creator_controller = FaqCreatorController(
        session=session,
        event_bus=event_bus,
        unit_of_work=unit_of_work,
        faq_repository=faq_repository,
        business_repository=business_repository,
        open_ai=open_ai,
    )

    response, code = await faq_creator_controller.create(
        id=UUID(faq_id),
        customer_id=UUID(customer_id),
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        is_active=True,
    )

    assert response.get("success") is True
    assert code == 201


@pytest.mark.asyncio
async def test_id_already_exist_on_faq_creator() -> None:
    faq_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"
    business_id = "c75e8241-2de8-462d-b673-cfd55c0edc0f"

    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    faq_repository = AsyncMock()
    faq_repository.get.return_value = Faq(
        id=UUID(faq_id),
        business_id=UUID(business_id),
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        embedding=[0.1] * 1536,
        is_active=True,
    )
    business_repository = AsyncMock()
    open_ai = _build_open_ai()

    faq_creator_controller = FaqCreatorController(
        session=session,
        event_bus=event_bus,
        unit_of_work=unit_of_work,
        faq_repository=faq_repository,
        business_repository=business_repository,
        open_ai=open_ai,
    )

    response, code = await faq_creator_controller.create(
        id=UUID(faq_id),
        customer_id=UUID(customer_id),
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        is_active=True,
    )

    assert response.get("success") is False
    assert code == 409


@pytest.mark.asyncio
async def test_business_does_not_exist_on_faq_creator() -> None:
    faq_id = "b6a34ed1-8997-4597-b152-7ec41e9ffbd2"
    customer_id = "611f6649-527b-4af1-8a1a-b66479b5eb2e"

    session = AsyncMock()
    event_bus = AsyncMock()
    unit_of_work = AsyncMock()
    faq_repository = AsyncMock()
    faq_repository.get.return_value = None
    business_repository = AsyncMock()
    business_repository.get_by_customer_id.return_value = None
    open_ai = _build_open_ai()

    faq_creator_controller = FaqCreatorController(
        session=session,
        event_bus=event_bus,
        unit_of_work=unit_of_work,
        faq_repository=faq_repository,
        business_repository=business_repository,
        open_ai=open_ai,
    )

    response, code = await faq_creator_controller.create(
        id=UUID(faq_id),
        customer_id=UUID(customer_id),
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        is_active=True,
    )

    assert response.get("success") is False
    assert code == 404
