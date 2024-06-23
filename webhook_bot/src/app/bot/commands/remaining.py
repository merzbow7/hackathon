import asyncio
import io
import json
import logging

import numpy as np
import pandas as pd
from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    BufferedInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keycloak import KeycloakAdmin

from app.adapters.sqlalchemy_db import User
from app.adapters.sqlalchemy_db.db import session_factory
from app.adapters.sqlalchemy_db.turnover.service import TurnoverService, ContractService, DictService
from app.application.diagram.ploting import make_remaining_diagram, make_predict_end_diagram, make_predict_buy_diagram
from app.application.predict.processing_user_requests import (
    processing_user_request_remainders,
    processing_user_request_time_to_finish_check,
    processing_user_request_time_to_finish,
    processing_json_calc_volume,
    prepare_json, processing_user_request_how_many,
)

logger = logging.getLogger()

remaining_router = Router()


class TurnoverState(StatesGroup):
    name = State()
    select = State()
    json = State()
    predict = State()
    year = State()


@remaining_router.message(F.text, Command("remaining"))
async def get_remaining_command(message: Message, state: FSMContext) -> None:
    await state.set_state(TurnoverState.name)
    await message.answer("Введите название товара", reply_markup=ReplyKeyboardRemove())


def get_remaining_kb() -> InlineKeyboardMarkup:
    end_button = InlineKeyboardButton(text="Когда закончится", callback_data="when_will_it_end")
    buy_button = InlineKeyboardButton(text="Сколько закупить", callback_data="how_much_need_buy")
    json_button = InlineKeyboardButton(text="Сформировать json", callback_data="make_json")
    builder = InlineKeyboardBuilder()
    builder.row(end_button)
    builder.row(buy_button, json_button)
    return builder.as_markup()


def get_remaining_buy_kb() -> InlineKeyboardMarkup:
    buy_button = InlineKeyboardButton(text="Сколько закупить", callback_data="how_much_need_buy")
    json_button = InlineKeyboardButton(text="Сформировать json", callback_data="make_json")
    builder = InlineKeyboardBuilder()
    builder.row(buy_button, json_button)
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
            await message.answer(remainder[1], reply_markup=get_remaining_buy_kb())
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
                output_str = end[1] + '\n' + res[1]
                df = res[2]
                buffer = await asyncio.to_thread(make_predict_end_diagram, df)
                photo = BufferedInputFile(buffer, filename="will_end.jpg")
                kb = get_remaining_kb()
                await callback.message.answer(output_str)
                await callback.bot.send_photo(callback.from_user.id, photo=photo, reply_markup=kb)


@remaining_router.callback_query(F.data == "how_much_need_buy")
async def get_buy(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        await state.set_state(TurnoverState.predict)
        await callback.message.answer("Введите период для которого нужна оценка в годах")


@remaining_router.message(TurnoverState.predict)
async def get_remaining_json_name(
    message: Message, state: FSMContext, db_user: User, kc_provider: KeycloakAdmin,
) -> None:
    data = await state.get_data()
    user_item = data.get("name")
    try:
        time_period = float(message.text.replace(",", "."))
    except TypeError:
        await message.answer("Это не число")
    else:
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
        res = processing_user_request_time_to_finish_check(df_contracts, df_directory, df_turnover_total, user_item)
        if res[0] == 1:
            await message.answer(res[1])
        else:
            items_list = res[2]
            res = processing_user_request_how_many(time_period, df_turnover_total, user_item, items_list)
            df = res[2]
            output_str = res[1]
            buffer = await asyncio.to_thread(make_predict_buy_diagram, df)
            photo = BufferedInputFile(buffer, filename="predict_buy.jpg")
            kb = get_remaining_kb()
            await message.bot.send_photo(message.from_user.id, photo=photo)
            await message.answer(output_str, reply_markup=kb)


@remaining_router.callback_query(F.data == "make_json")
async def get_remaining_json(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    try:
        await callback.bot.answer_callback_query(callback.id)
    except TelegramBadRequest as exc:
        logger.error(exc.message)
    else:
        await state.set_state(TurnoverState.json)
        await callback.message.answer("Введите период для которого нужен прогноз")


def json_numpy_converter(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Преобразует массив NumPy в список
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)  # Преобразует число NumPy в стандартное целое число Python
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)  # Преобразует число с плавающей точкой NumPy в стандартное число с плавающей точкой Python
    elif isinstance(obj, np.bool_):
        return bool(obj)  # Преобразует булево значение NumPy в стандартное булево значение Python
    else:
        return obj


def get_json_file(json_data: dict, filename: str = "data.json") -> BufferedInputFile:
    json_buffer = io.StringIO()
    json.dump(json_data, json_buffer, ensure_ascii=False, default=json_numpy_converter)
    json_buffer.seek(0)
    return BufferedInputFile(file=json_buffer.getvalue().encode(), filename=filename)


@remaining_router.message(TurnoverState.json)
async def get_remaining_json_name(
    message: Message, state: FSMContext, db_user: User, kc_provider: KeycloakAdmin,
) -> None:
    data = await state.get_data()
    user_item = data.get("name")
    try:
        time_period = float(message.text.replace(",", "."))
    except TypeError:
        await message.answer("Это не число")
    else:
        kc_user = await kc_provider.a_get_user(user_id=db_user.keycloak_id)
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

        res = processing_json_calc_volume(
            time_period, df_contracts, df_directory, df_turnover_total, user_item
        )
        if res[0] == 1:
            await message.answer(res[1])
        elif res[0] == 2:
            await message.answer(res[1])
        else:
            output_str = res[1]
            df_tmp_res = res[2]
            total_volume = res[3]
            total_price = res[4]
            okei_code = res[5]

            json_dict = prepare_json(
                df_turnover_total,
                df_contracts,
                df_directory,
                user_item,
                total_volume,
                total_price,
                okei_code,
            )
            json_dict["CustomerId"] = message.from_user.id
            json_dict["TelegramUsername"] = message.from_user.username
            json_dict["CustomerName"] = f'{kc_user.get("firstName")} {kc_user.get("lastName")}'

            filename = f"{user_item}_{time_period}_лет.json"
            json_file = get_json_file(json_dict, filename)
            await message.answer_document(json_file)
            await message.answer(output_str, reply_markup=get_remaining_kb())
