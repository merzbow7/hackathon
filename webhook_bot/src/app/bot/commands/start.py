from urllib.parse import urljoin

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.adapters.sqlalchemy_db.users.interactor import create_user_use_case
from app.config.settings import Settings

start_router = Router()


async def auth_case(message: Message, settings: Settings):
    builder = InlineKeyboardBuilder()

    verification_code = await create_user_use_case(message.from_user.id)
    if settings.skip_auth and verification_code:
        await message.answer("Вы авторизованы. Можете приступать к работе")
        return

    path = f"/sync/{verification_code}"

    url = urljoin(settings.frontend_url, path)

    builder.row(
        InlineKeyboardButton(
            text="Нажмите на кнопку чтобы пройти авторизацию",
            url=url
        )
    )
    await message.answer(
        "Работа с данным ботом доступна только авторизованным пользователям.",
        reply_markup=builder.as_markup()
    )


@start_router.message(CommandStart())
async def start(message: Message, settings: Settings) -> None:
    await auth_case(message, settings)
