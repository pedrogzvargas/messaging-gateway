import asyncio
from sqlalchemy import select
from langchain_openai import OpenAIEmbeddings
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from sqlalchemy_models import FAQModel

async def query_faqs():
    environ = PyEnviron()

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", api_key=environ.get_str("OPENAI_API_KEY"))

    db_values = dict(
        dialect=environ.get_str("POSTGRES_DIALECT"),
        driver=environ.get_str("POSTGRES_DRIVER"),
        host=environ.get_str("POSTGRES_HOST"),
        user=environ.get_str("POSTGRES_USER"),
        password=environ.get_str("POSTGRES_PASSWORD"),
        port=environ.get_str("POSTGRES_PORT"),
        db=environ.get_str("POSTGRES_DB"),
        echo=environ.get_bool("SQL_ECHO", False),
    )

    query = "Que servicios ofrecen?"
    query_embedding = await embedding_model.aembed_query(
        query
    )

    stmt = (
        select(FAQModel)
        .where(
            FAQModel.service == "general"
        )
        .order_by(
            FAQModel.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(2)
    )

    async with AsyncAlchemySessionCreator(**db_values).get_session() as session:
        result = await session.execute(stmt)
        faqs = result.scalars().all()
        for faq in faqs:
            print(faq)

if __name__ == "__main__":
    asyncio.run(query_faqs())
