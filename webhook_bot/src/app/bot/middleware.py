from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, User

from app.adapters.sqlalchemy_db.users.repository import get_user_repo
from app.bot.commands.start import auth_case


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
        app = data.get("app")
        if not telegram_user:
            return await auth_case(message=event.message, app=app)

        user_repo = get_user_repo()
        user = await user_repo.get_verified_user(telegram_user.id)
        if not user:
            return await auth_case(message=event.message, app=app)

        return await handler(event, data)
