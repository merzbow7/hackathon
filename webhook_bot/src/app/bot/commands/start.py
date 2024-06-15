from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.adapters.sqlalchemy_db.users.interactor import create_user_use_case
from app.application.url_builder.builder import UrlBuilder
from app.bot.keyboard.commands_kb import get_commands_kb
from app.config.settings import Settings

start_router = Router()


async def auth_case(message: Message, settings: Settings):
    builder = InlineKeyboardBuilder()

    verification_code = await create_user_use_case(message.from_user.id)

    url_builder = UrlBuilder(
        base_url=settings.base_url,
        path="/api/auth/registration",
        query={"code": verification_code}
    )

    builder.row(
        InlineKeyboardButton(
            text="Нажмите на кнопку чтобы пройти авторизацию",
            url=url_builder.url
        )
    )
    await message.answer(
        "Работа с данным ботом доступна только авторизованным пользователям.",
        reply_markup=builder.as_markup()
    )


@start_router.message(CommandStart())
async def start(message: Message, settings: Settings) -> None:
    await auth_case(message, settings)


async def enjoy_bot(bot: Bot, telegram_id: int):
    await bot.send_message(telegram_id, "Вы авторизованы", reply_markup=get_commands_kb())
