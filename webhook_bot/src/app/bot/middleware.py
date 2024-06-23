from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, User

from app.adapters.sqlalchemy_db.users.repository import get_user_repo
from app.bot.commands.start import auth_case
from app.config.settings import Settings
from app.main.keycloak_provider import get_keycloak_admin_provider


class AuthMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        telegram_user: User = data.get("event_from_user")
        settings: Settings = data.get("settings")
        if not telegram_user:
            return await auth_case(message=event.message, settings=settings)

        user_repo = get_user_repo()
        user = await user_repo.get_verified_user(telegram_user.id)
        if not user:
            return await auth_case(message=event.message, settings=settings)

        data["db_user"] = user
        data["kc_provider"] = get_keycloak_admin_provider()
        return await handler(event, data)
