import uuid

from app.adapters.sqlalchemy_db import User
from app.adapters.sqlalchemy_db.users.repository import get_user_repo
from app.config.settings import get_settings


async def create_user_use_case(telegram_id: int, default_institution: int = 1) -> uuid.UUID:
    repo = get_user_repo()
    db_user = await repo.get_by_telegram(telegram_id)

    if db_user and db_user.telegram_id:
        return db_user.verification_code
    settings = get_settings()
    if settings.skip_auth:
        user = User(telegram_id=telegram_id, keycloak_id=uuid.uuid4(), institution_id=default_institution)
    else:
        user = User(telegram_id=telegram_id)
    await repo.add(user)
    return user.verification_code
