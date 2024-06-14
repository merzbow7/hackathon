import uuid

from app.adapters.sqlalchemy_db import User
from app.adapters.sqlalchemy_db.users.repository import get_user_repo


async def create_user_use_case(telegram_id: int) -> uuid.UUID:
    repo = get_user_repo()
    db_user = await repo.get_by_telegram(telegram_id)

    if db_user and db_user.telegram_id:
        return db_user.verification_code

    user = User(telegram_id=telegram_id)
    await repo.add(user)
    return user.verification_code


async def verification_use_case(code: uuid.UUID) -> bool:
    repo = get_user_repo()
    db_user = await repo.verify(code)
    return bool(db_user)
