import json
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_models import RoleModel
from sqlalchemy_models import PermissionModel
from sqlalchemy_models import RolePermissionModel
from sqlalchemy_models import ChannelModel
from modules.shared.environ.infrastructure import PyEnviron
from modules.shared.persistence.infrastructure import AsyncAlchemySessionCreator
from sqlalchemy.dialects.postgresql import insert


FIXTURES_PATH = Path(__file__).parent.parent / 'fixtures'

MODEL_MAP = {
    "role": RoleModel,
    "permission": PermissionModel,
    "role_permission": RolePermissionModel,
    "channel": ChannelModel,
}

async def load_fixture(session: AsyncSession, file_path: Path) -> None:
    fixture = file_path.stem
    model = MODEL_MAP.get(fixture.split("_", 1)[-1])

    if not model:
        print(f"Model {fixture} not found.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    stmt = insert(model).values(data)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["id"]
    )
    await session.execute(stmt)

    print(f"Loaded {len(data)} records from {file_path.name}")

async def seed() -> None:
    environ = PyEnviron()
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
    async with AsyncAlchemySessionCreator(**db_values).get_session() as session:
        for file_path in sorted(FIXTURES_PATH.glob("*.json")):
            await load_fixture(session, file_path)

            await session.commit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
