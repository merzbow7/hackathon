from aiogram.types import CallbackQuery


async def get_remaining_diagram(callback: CallbackQuery):
    print(callback.message)
    await callback.answer("Рисуем")
