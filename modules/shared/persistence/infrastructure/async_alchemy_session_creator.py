from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


class AsyncAlchemySessionCreator:
    """
    Async Alchemy Database Session Creator
    """

    _instance = None

    def __new__(cls, dialect: str, driver: str, host: str, user: str, password: str, port: int, db: str, echo: bool = False):
        if cls._instance is None:
            cls._instance = super(AsyncAlchemySessionCreator, cls).__new__(cls)
            cls._instance._init_session(
                dialect=dialect,
                driver=driver,
                host=host,
                user=user,
                password=password,
                port=port,
                db=db,
                echo=echo,
            )

        return cls._instance

    def _init_session(self, dialect: str, driver: str, host: str, user: str, password: str, port: int, db: str, echo: bool = False):
        self.url_database = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{db}"
        self.engine = create_async_engine(self.url_database, echo=echo)

        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    def get_session(self):
        return self.SessionLocal()

    def get_url_database(self):
        return self.url_database
