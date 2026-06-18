from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class AlchemySessionCreator:
    """
    Alchemy Database Session Creator
    """

    _instance = None

    def __new__(cls, dialect: str, driver: str, host: str, user: str, password: str, port: int, db: str):
        if cls._instance is None:
            cls._instance = super(AlchemySessionCreator, cls).__new__(cls)
            cls._instance._init_session(
                dialect=dialect,
                driver=driver,
                host=host,
                user=user,
                password=password,
                port=port,
                db=db,
            )

        return cls._instance

    def _init_session(self, dialect: str, driver: str, host: str, user: str, password: str, port: int, db: str):
        self.url_database = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{db}"
        engine = create_engine(self.url_database, echo=True)
        self.session = Session(bind=engine)

    def get_session(self):
        return self.session

    def get_url_database(self):
        return self.url_database
