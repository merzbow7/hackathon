from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db.models import Turnover, User, Dict, Contract


class TurnoverService:

    def __init__(self, user: User, session: AsyncSession):
        self.user = user
        self.session = session

    async def find_product(self):
        stmt = select(Turnover.__table__.columns).where(
            Turnover.institution_id == self.user.institution_id,
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()


class DictService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        stmt = select(Dict.__table__.columns)
        result = await self.session.execute(stmt)
        return result.mappings().all()


class ContractService:

    def __init__(self, user: User, session: AsyncSession):
        self.user = user
        self.session = session

    async def get_all(self):
        stmt = select(Contract.__table__.columns).where(
            Contract.institution_id == self.user.institution_id,
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()
