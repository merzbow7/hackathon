from functools import lru_cache

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


@lru_cache
def get_commands_kb():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="🧮 Остатки", callback_data="remaining_callback"),
        InlineKeyboardButton(text="💾 JSON", callback_data="json_pack_callback")
    )
    kb.row(
        InlineKeyboardButton(text="📈 Прогноз", callback_data="predict_callback"),
    )
    return kb.as_markup()
