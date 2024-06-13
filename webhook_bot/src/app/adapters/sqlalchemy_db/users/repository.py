import uuid

from sqlalchemy import select, update

from app.adapters.sqlalchemy_db import TelegramUser
from app.adapters.sqlalchemy_db.db import AsyncSessionMaker
from app.application.models.telegram_user import User


class UserRepository:
    def __init__(self, session: AsyncSessionMaker):
        self.session = session

    async def add(self, user: User):
        async with self.session() as session:
            session.add(user)
            await session.commit()

    async def get(self, telegram_id: int) -> User:
        async with self.session() as session:
            stmt = select(User).where(
                TelegramUser.telegram_id == telegram_id,
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_verified_user(self, telegram_id: int) -> User:
        async with self.session() as session:
            stmt = select(User).where(
                TelegramUser.telegram_id == telegram_id,
                TelegramUser.keycloak_id.isnot(None),
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def verify(self, verification_code: uuid.UUID) -> User:
        async with self.session() as session:
            stmt = select(User).where(
                TelegramUser.verification_code == verification_code,
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                update_stmt = update(
                    TelegramUser
                ).values(
                    {"keycloak_id": uuid.uuid4()}
                ).where(TelegramUser.id == user.id)
                await session.execute(update_stmt)
                await session.commit()

            return user
