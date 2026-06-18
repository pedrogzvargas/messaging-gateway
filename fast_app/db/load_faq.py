import json
from uuid import UUID
import asyncio
from langchain_openai import OpenAIEmbeddings
from sqlalchemy_models import FAQModel
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator

async def load_faqs():
    with open("faqs.json", "r", encoding="utf-8") as f:
        faqs = json.load(f)

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

    faq_instances = []
    for faq in faqs:
        embedding = await embedding_model.aembed_query(
            f"""
            Pregunta:
            {faq['question']}

            Respuesta:
            {faq['answer']}
            """
        )

        faq = FAQModel(
            id=UUID(faq.get("id")),
            question=faq.get("question"),
            answer=faq.get("answer"),
            service=faq.get("service"),
            embedding=embedding
        )

        faq_instances.append(faq)

    async with AsyncAlchemySessionCreator(**db_values).get_session() as session:
        session.add_all(faq_instances)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(load_faqs())
