from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from .config import get_settings

async def get_session():
    settings = get_settings()
    db_values = dict(
        dialect=settings.postgres_dialect,
        driver=settings.postgres_driver,
        host=settings.postgres_host,
        user=settings.postgres_user,
        password=settings.postgres_password,
        port=settings.postgres_port,
        db=settings.postgres_db,
        echo=settings.sql_echo,
    )

    async with AsyncAlchemySessionCreator(**db_values).get_session() as session:
        yield session
