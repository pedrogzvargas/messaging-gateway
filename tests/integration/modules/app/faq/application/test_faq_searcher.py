from uuid import UUID
import pytest
from modules.app.faq.infrastructure import PgFaqRepository
from modules.app.faq.application import FaqSearcher
from sqlalchemy_models import FAQModel
from sqlalchemy_models import BusinessModel
from sqlalchemy_models import CustomerModel
from sqlalchemy_models import UserModel
from tests.integration.fixtures import db_session


async def _seed_business(db_session):
    user = UserModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        email="demo@noemail.com",
        password="test",
        is_active=True,
    )
    customer = CustomerModel(
        id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        name="Pedro",
        last_name="Gonzalez"
    )
    business = BusinessModel(
        id=UUID("c75e8241-2de8-462d-b673-cfd55c0edc0f"),
        customer_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
        name="Vualdex",
    )
    db_session.add_all([user, customer, business])

    return business


def _build_searcher(db_session):
    return FaqSearcher(faq_repository=PgFaqRepository(db_session))


@pytest.mark.asyncio
async def test_no_faqs_on_faq_searcher(db_session):
    await _seed_business(db_session)

    faq_searcher = _build_searcher(db_session)
    faqs_result = await faq_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert faqs_result.limit == 10
    assert faqs_result.page == 1
    assert faqs_result.pages == 0
    assert faqs_result.total == 0
    assert len(faqs_result.items) == 0


@pytest.mark.asyncio
async def test_no_filters_on_faq_searcher(db_session):
    business = await _seed_business(db_session)
    faq_1 = FAQModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        business_id=business.id,
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        is_active=True,
        embedding=[0.1] * 1536,
    )
    faq_2 = FAQModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        business_id=business.id,
        question="What are your business hours?",
        answer="We are open 9 to 5",
        is_active=True,
        embedding=[0.2] * 1536,
    )
    db_session.add_all([faq_1, faq_2])

    faq_searcher = _build_searcher(db_session)
    faqs_result = await faq_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert faqs_result.limit == 10
    assert faqs_result.page == 1
    assert faqs_result.pages == 1
    assert faqs_result.total == 2
    assert len(faqs_result.items) == 2


@pytest.mark.asyncio
async def test_filter_by_question_on_faq_searcher(db_session):
    business = await _seed_business(db_session)
    faq_1 = FAQModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        business_id=business.id,
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        is_active=True,
        embedding=[0.1] * 1536,
    )
    faq_2 = FAQModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        business_id=business.id,
        question="What are your business hours?",
        answer="We are open 9 to 5",
        embedding=[0.2] * 1536,
        is_active=True,
    )
    db_session.add_all([faq_1, faq_2])

    faq_searcher = _build_searcher(db_session)
    faqs_result = await faq_searcher.search(
        query_params={"question": "password"},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert faqs_result.limit == 10
    assert faqs_result.page == 1
    assert faqs_result.pages == 1
    assert faqs_result.total == 1
    assert len(faqs_result.items) == 1
    assert faqs_result.items[0].question == "How do I reset my password?"

@pytest.mark.asyncio
async def test_search_scopes_results_to_the_user_business(db_session):
    business_1 = await _seed_business(db_session)
    other_user = UserModel(
        id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        email="other@noemail.com",
        password="test",
        is_active=True,
    )
    other_customer = CustomerModel(
        id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        user_id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        name="Other",
        last_name="Owner"
    )
    business_2 = BusinessModel(
        id=UUID("9b2f4c5d-6e7f-4a8b-9c1d-2e3f4a5b6c7d"),
        customer_id=UUID("7e6b7f3a-0d1a-4a2a-9a7a-2f3b4c5d6e7f"),
        name="Other Business",
    )
    db_session.add_all([other_user, other_customer, business_2])

    faq_1 = FAQModel(
        id=UUID("41ad6238-a88f-495a-9254-cca57fbb735b"),
        business_id=business_1.id,
        question="How do I reset my password?",
        answer="Click on 'forgot password'",
        is_active=True,
        embedding=[0.1] * 1536,
    )
    faq_2 = FAQModel(
        id=UUID("3d9400dc-206a-4301-8e19-099fc5d28b18"),
        business_id=business_2.id,
        question="Do you ship internationally?",
        answer="Yes, we do",
        is_active=True,
        embedding=[0.2] * 1536,
    )
    db_session.add_all([faq_1, faq_2])

    faq_searcher = _build_searcher(db_session)
    faqs_result = await faq_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert faqs_result.total == 1
    assert len(faqs_result.items) == 1
    assert faqs_result.items[0].question == "How do I reset my password?"


@pytest.mark.asyncio
async def test_search_returns_empty_when_user_has_no_business(db_session):
    faq_searcher = _build_searcher(db_session)
    faqs_result = await faq_searcher.search(
        query_params={},
        user_id=UUID("611f6649-527b-4af1-8a1a-b66479b5eb2e"),
    )

    assert faqs_result.total == 0
    assert faqs_result.pages == 0
    assert len(faqs_result.items) == 0
