from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.adapters.sqlalchemy_db.db import session_factory
from app.adapters.sqlalchemy_db.models import Institution


class InstitutionRepository:
    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    async def get_all(self):
        async with self.session_maker() as session:
            stmt = select(Institution)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get(self, institution_id: int):
        async with self.session_maker() as session:
            stmt = select(Institution).where(Institution.id == institution_id)
            result = await session.execute(stmt)
            return result.scalars().one_or_none()

    async def add(self, name: str):
        async with self.session_maker() as session:
            institution = Institution(name=name)
            session.add(institution)
            await session.commit()
            return institution.id


def get_institution_repo() -> InstitutionRepository:
    return InstitutionRepository(session_factory)
