import asyncio
import logging
from typing import Any

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (BufferedInputFile, CallbackQuery,
                           InlineKeyboardButton, Message, ReplyKeyboardRemove)
from aiogram.utils.formatting import Bold, Text, as_list, as_marked_section
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.adapters.sqlalchemy_db import User
from app.adapters.sqlalchemy_db.turnover.service import TurnoverService
from app.application.diagram.ploting import make_remaining_diagram
from app.bot.data.remaining_data import remaining_dict
from app.bot.keyboard.commands_kb import get_commands_kb

logger = logging.getLogger()

remaining_router = Router()


class TurnoverState(StatesGroup):
    name = State()
    select = State()
    product = State()


def get_remaining_product_list(products: list[dict[str, Any]]) -> Text:
    rows = [
        f"Номер:{product.get('id')} - {product.get('product')}" for product in products
    ]
    return as_list(
        as_marked_section(
            Bold("Введите номер товара для просмотра остатков\nПо вашему запросу найдены товары:"),
            *rows,
            marker="✅ "
        )
    )


async def get_remaining(message: Message, state: FSMContext) -> None:
    await state.set_state(TurnoverState.name)
    await message.answer("Введите название товара")


@remaining_router.message(F.text, Command("remaining"))
async def get_remaining_command(message: Message, state: FSMContext) -> None:
    await state.set_state(TurnoverState.name)
    await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())


@remaining_router.message(TurnoverState.name)
async def get_remaining_name(message: Message, state: FSMContext, db_user: User) -> None:
    await state.update_data(name=message.text)
    await state.set_state(TurnoverState.select)
    service = TurnoverService(db_user)
    products = await service.find_product(message.text)
    print(f"{products=}")
    if products:
        product_list = get_remaining_product_list(products)
        await message.answer(product_list.as_html())
    else:
        await message.answer("Не найдено")


@remaining_router.message(TurnoverState.select)
async def get_remaining_product(message: Message, state: FSMContext, db_user: User) -> None:
    await state.update_data(name=message.text)
    await state.set_state(TurnoverState.product)
    service = TurnoverService(db_user)
    product = await service.get_remaining(int(message.text))
    if product:
        answer = as_list(
            Bold(product.product),
            f"Остаток: {product.quantity_end_debit} {product.unit_of_measurement}"
        )
        await message.answer(answer.as_html())
    else:
        await message.answer("Не найдено")


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
