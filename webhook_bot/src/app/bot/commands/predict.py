import asyncio
import logging
import random

import pandas as pd
from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, BufferedInputFile
from aiogram.utils.formatting import as_list, as_marked_section, Bold, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.application.diagram.ploting import make_predict_diagram

from app.bot.keyboard.commands_kb import get_commands_kb

logger = logging.getLogger()

predict_router = Router()


def get_predict_data() -> dict[str, dict]:
    predict_dict = {
        "Учебники": 25,
        "Письменные принадлежности": 120,
        "Осветительные приборы": 5,
    }
    return {
        i.strftime("%Y-%m"): {k: v * random.randint(10, 15) for k, v in predict_dict.items()}
        for i in pd.date_range(start="1/1/2023", end="31/12/2023", freq="QS")
    }


def dataframe_to_markdown(df: pd.DataFrame) -> list[str]:
    df_index = df.index.to_series()
    idx_max = len(df_index.apply(len).idxmax())
    # Преобразуем датафрэйм в строку
    df_str = df.to_string(index=False)
    # Разделяем строки и находим максимальные длины колонок
    lines = df_str.split('\n')
    max_lengths = 7
    # Форматируем строки с учетом максимальных длин колонок
    formatted_lines = []
    for idx, line in enumerate(lines):
        words = line.split()
        if idx == 0:
            index_part = " ".ljust(idx_max)
        else:
            index_part = df_index.iloc[idx - 1].ljust(idx_max)

        index_part = index_part[:12] + " |"

        formatted_line = index_part + "|".join([i.ljust(max_lengths) for i in words])
        formatted_line.replace(" ", "&nbsp;")
        formatted_lines.append(formatted_line)
    return formatted_lines


def get_predict_content() -> Text:
    content = get_predict_data()
    df = pd.DataFrame(content)
    mkd = dataframe_to_markdown(df)
    return as_list(
        as_marked_section(
            Bold("Прогноз:"),
            *mkd,
            marker="✅ "
        )
    )


async def get_predict(message: Message) -> None:
    diagram_button = InlineKeyboardButton(text="Диаграмма прогноза", callback_data='predict_diagram_button')
    builder = InlineKeyboardBuilder()
    builder.row(diagram_button)

    content = get_predict_content()
    await message.answer(text=content.as_html(), reply_markup=builder.as_markup())


@predict_router.message(F.text, Command("predict"))
async def get_remaining_command(message: Message) -> None:
    return await get_predict(message)


@predict_router.callback_query(F.data == "predict_callback")
async def get_remaining_callback(callback: CallbackQuery) -> None:
    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        return await get_predict(callback.message)


@predict_router.callback_query(F.data == "predict_diagram_button")
async def get_predict_diagram(callback: CallbackQuery):
    data = get_predict_data()

    buffer = await asyncio.to_thread(make_predict_diagram, data)
    photo = BufferedInputFile(buffer, filename="Прогноз.png")

    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=get_commands_kb())
