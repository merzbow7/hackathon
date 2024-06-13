import io
import json
import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from app.bot.data.remaining_data import remaining_dict
from app.bot.keyboard.commands_kb import get_commands_kb
from app.main.typed import FastApiApp

json_router = Router()
logger = logging.getLogger()


def get_json_file() -> BufferedInputFile:
    json_buffer = io.StringIO()
    json.dump(remaining_dict, json_buffer, ensure_ascii=False)
    json_buffer.seek(0)
    return BufferedInputFile(file=json_buffer.getvalue().encode(), filename="data.json")


@json_router.message(F.text, Command("json_pack"))
async def get_json(message: Message, app: FastApiApp) -> None:
    file = get_json_file()
    await message.answer_document(file, reply_markup=get_commands_kb())


@json_router.callback_query(F.data == "json_pack_callback")
async def get_json_callback(callback: CallbackQuery) -> None:
    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        file = get_json_file()
        await callback.message.answer_document(file, reply_markup=get_commands_kb())
