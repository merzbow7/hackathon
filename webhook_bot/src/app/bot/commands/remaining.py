import asyncio
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import (BufferedInputFile, CallbackQuery,
                           InlineKeyboardButton, Message)
from aiogram.utils.formatting import Bold, Text, as_list, as_marked_section
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.application.diagram.ploting import make_remaining_diagram
from app.bot.data.remaining_data import remaining_dict
from app.bot.keyboard.commands_kb import get_commands_kb

logger = logging.getLogger()

remaining_router = Router()


def get_remaining_content() -> Text:
    items = [f"{key}: {value}" for key, value in remaining_dict.items()]
    return as_list(
        as_marked_section(
            Bold("Остатки:"),
            *items,
            marker="✅ "
        )
    )


async def get_remaining(message: Message) -> None:
    content = get_remaining_content()
    diagram_button = InlineKeyboardButton(text="Диаграмма остатков", callback_data='remaining_diagram_button')
    builder = InlineKeyboardBuilder()
    builder.row(diagram_button)
    await message.answer(content.as_html(), reply_markup=builder.as_markup())


@remaining_router.message(F.text, Command("remaining"))
async def get_remaining_command(message: Message) -> None:
    return await get_remaining(message)


@remaining_router.callback_query(F.data == "remaining_callback")
async def get_remaining_callback(callback: CallbackQuery) -> None:
    await callback.bot.answer_callback_query(callback.id)
    return await get_remaining(callback.message)


@remaining_router.callback_query(F.data == "remaining_diagram_button")
async def get_remaining_diagram(callback: CallbackQuery):
    data = [{"name": k, "count": v} for k, v in remaining_dict.items()]

    buffer = await asyncio.to_thread(make_remaining_diagram, data)
    photo = BufferedInputFile(buffer, filename="Остатки.png")

    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=get_commands_kb())
