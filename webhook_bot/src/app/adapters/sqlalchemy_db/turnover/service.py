from sqlalchemy import select

from app.adapters.sqlalchemy_db.db import session_factory
from app.adapters.sqlalchemy_db.models import Turnover, User


class TurnoverService:

    def __init__(self, user: User):
        self.user = user

    async def find_product(self, name: str):
        like_template = "%{}%"
        parts = "%".join(name.split())
        escaped_template = like_template.format(parts)
        stmt = select(Turnover.id, Turnover.product).where(
            Turnover.product.ilike(escaped_template),
            Turnover.quarter_number == 4,
            Turnover.quantity_end_debit > 0,
            Turnover.institution_id == self.user.institution_id,
        )
        async with session_factory() as session:
            result = await session.execute(stmt)
            return result.mappings().all()

    async def get_remaining(self, idx: int) -> Turnover:
        stmt = select(
            Turnover
        ).where(
            Turnover.id == idx,
            Turnover.quarter_number == 4,
            Turnover.institution_id == self.user.institution_id,
        ).limit(1)
        async with session_factory() as session:
            result = await session.execute(stmt)
            return result.scalars().one_or_none()
