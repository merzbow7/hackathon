import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import selectinload

from app.adapters.sqlalchemy_db import User
from app.adapters.sqlalchemy_db.db import session_factory


class UserRepository:
    def __init__(self, session: async_sessionmaker):
        self.session = session

    async def get_all(self):
        async with self.session() as session:
            stmt = select(User).options(selectinload(User.institution))
            result = await session.execute(stmt)
            return result.scalars().all()

    async def add(self, user: User):
        async with self.session() as session:
            session.add(user)
            await session.commit()

    async def get_by_id(self, user_id: int) -> User:
        async with self.session() as session:
            stmt = select(User).options(
                selectinload(User.institution),
            ).where(
                User.id == user_id,
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def set_institution(self, user_id: int, institution_id: int | None):
        stmt = update(User).values(
            {"institution_id": institution_id},
        ).where(
            User.id == user_id,
        ).returning(User.id)
        async with self.session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one_or_none()

    async def get_by_telegram(self, telegram_id: int) -> User:
        async with self.session() as session:
            stmt = select(User).where(
                User.telegram_id == telegram_id,
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_verified_user(self, telegram_id: int) -> User:
        async with self.session() as session:
            stmt = select(User).where(
                User.telegram_id == telegram_id,
                User.keycloak_id.isnot(None),
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def verify(self, verification_code: uuid.UUID, keycloak_id: uuid.UUID) -> User:
        async with self.session() as session:
            stmt = select(User).options(selectinload(User.institution)).where(
                User.verification_code == verification_code,
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                update_stmt = update(
                    User
                ).values(
                    {"keycloak_id": keycloak_id}
                ).where(User.id == user.id)
                await session.execute(update_stmt)
                await session.commit()

            return user


def get_user_repo() -> UserRepository:
    return UserRepository(session_factory)
