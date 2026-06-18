from modules.shared.persistence.domain import UnitOfWork
from .alchemy_error_translator import AlchemyErrorTranslator


class AlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        self.session = self.session
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.rollback()
            raise AlchemyErrorTranslator.translate(exc)
        await self.commit()

    def get_session(self):
        return self.session

    async def commit(self):
        await self.session.commit()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()
        await self.session.close()
