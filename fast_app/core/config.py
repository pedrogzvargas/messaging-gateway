from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "FastAPI"
    debug: bool = False
    wa_verify_token: str
    # POSTGRES
    postgres_dialect: str = "postgresql"
    postgres_driver: str = "asyncpg"
    postgres_host: str
    postgres_user: str
    postgres_password: str
    postgres_port: int
    postgres_db: str
    sql_echo: bool = True
    # REDIS
    redis_host: str
    redis_port: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="allow",
    )

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for {settings.app_name}")
    return settings
