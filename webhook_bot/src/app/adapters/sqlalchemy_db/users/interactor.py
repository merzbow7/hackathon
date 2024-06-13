import uuid

from app.adapters.sqlalchemy_db.users.repository import UserRepository
from app.application.models.telegram_user import User
from app.main.typed import FastApiApp


async def create_user_use_case(telegram_id: int, app: FastApiApp) -> uuid.UUID:
    repo = UserRepository(session=app.async_session)
    db_user = await repo.get(telegram_id)

    if db_user and db_user.telegram_id:
        return db_user.verification_code

    user = User(telegram_id=telegram_id)
    await repo.add(user)
    return user.verification_code


async def verification_use_case(code: uuid.UUID, app: FastApiApp) -> bool:
    repo = UserRepository(session=app.async_session)
    db_user = await repo.verify(code)
    return bool(db_user)
