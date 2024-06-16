import asyncio
import logging
from typing import Any

import pandas as pd
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, BufferedInputFile, InlineKeyboardButton, InlineKeyboardMarkup, \
    CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.adapters.sqlalchemy_db import User
from app.adapters.sqlalchemy_db.db import session_factory
from app.adapters.sqlalchemy_db.turnover.service import TurnoverService, ContractService, DictService
from app.application.diagram.ploting import make_remaining_diagram, make_predict_diagram
from app.application.predict.processing_user_requests import processing_user_request_remainders, \
    processing_user_request_time_to_finish_check, processing_user_request_time_to_finish

logger = logging.getLogger()

remaining_router = Router()


class TurnoverState(StatesGroup):
    name = State()
    select = State()


@remaining_router.message(F.text, Command("remaining"))
async def get_remaining_command(message: Message, state: FSMContext) -> None:
    await state.set_state(TurnoverState.name)
    await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())


def get_remaining_kb() -> InlineKeyboardMarkup:
    end_button = InlineKeyboardButton(text="когда закончится", callback_data="when_will_it_end")
    json_button = InlineKeyboardButton(text="Сформировать json", callback_data="make_json")
    builder = InlineKeyboardBuilder()
    builder.row(end_button, json_button)
    return builder.as_markup()


@remaining_router.message(TurnoverState.name)
async def get_remaining_name(message: Message, state: FSMContext, db_user: User) -> None:
    await state.update_data(name=message.text)
    await state.set_state(TurnoverState.select)
    async with session_factory() as session:
        service = TurnoverService(db_user, session)
        products = await service.find_product()

    if products:
        df = pd.DataFrame(products)
        remainder = processing_user_request_remainders(df, message.text)
        if remainder[0] != 1:
            buffer = await asyncio.to_thread(make_remaining_diagram, remainder[-1])
            photo = BufferedInputFile(buffer, filename="Остаток.jpg")
            kb = get_remaining_kb()
            await message.bot.send_photo(message.from_user.id, photo=photo, caption=remainder[1], reply_markup=kb)
        else:
            await message.answer(remainder[1])
    else:
        await message.answer("Не найдено")


@remaining_router.callback_query(F.data == "when_will_it_end")
async def get_remaining_end(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    data = await state.get_data()
    user_item = data.get("name")

    async with session_factory() as session:
        turnover_service = TurnoverService(db_user, session)
        products = await turnover_service.find_product()
        df_turnover_total = pd.DataFrame(products)

        dict_service = DictService(session)
        directory = await dict_service.get_all()
        df_directory = pd.DataFrame(directory)

        contract_service = ContractService(db_user, session)
        contracts = await contract_service.get_all()
        df_contracts = pd.DataFrame(contracts)

    end = processing_user_request_time_to_finish_check(
        df_contracts, df_directory, df_turnover_total, user_item,
    )
    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        if end[0] == 1:
            await callback.message.answer(text=end[1])
        else:
            items_list = end[2]
            res = processing_user_request_time_to_finish(df_turnover_total, user_item, items_list)

            if res[0] == 1:
                await callback.message.answer(text=res[1])
            else:
                output_str = res[1]
                df = res[2]
                buffer = await asyncio.to_thread(make_predict_diagram, df)
                photo = BufferedInputFile(buffer, filename="will_end.jpg")
                kb = get_remaining_kb()
                await callback.bot.send_photo(
                    callback.from_user.id, photo=photo, caption=output_str, reply_markup=kb
                )
