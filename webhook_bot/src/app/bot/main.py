from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types

from app.bot.middleware import AuthMiddleware
from app.bot.router import bot_router
from app.main.typed import FastApiApp


async def get_bot(app: FastApiApp) -> tuple[Dispatcher, Bot]:
    bot = Bot(token=app.settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.update.outer_middleware(AuthMiddleware())
    dp.include_routers(bot_router)
    app.bot = bot
    app.dp = dp

    await bot.set_my_commands(
        [
            types.BotCommand(command="/start", description="Запуск бота"),
            types.BotCommand(command="/remaining", description="Посмотреть остатки"),
            types.BotCommand(command="/predict", description="Посмотреть прогноз"),
        ]
    )

    return dp, bot
