from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import FastAPI

from app.adapters.sqlalchemy_db.users.interactor import create_user_use_case
from app.application.url_builder.builder import UrlBuilder
from app.bot.keyboard.commands_kb import get_commands_kb
from app.main.typed import FastApiApp

start_router = Router()


async def auth_case(message: Message, app: FastApiApp):
    builder = InlineKeyboardBuilder()

    verification_code = await create_user_use_case(message.from_user.id, app=app)

    url_builder = UrlBuilder(
        base_url=app.settings.base_url,
        path=app.url_path_for("register_telegram_user"),
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
async def start(message: Message, app: FastAPI) -> None:
    await auth_case(message, app)


async def enjoy_bot(bot: Bot, telegram_id: int):
    await bot.send_message(telegram_id, "Вы авторизованы", reply_markup=get_commands_kb())
