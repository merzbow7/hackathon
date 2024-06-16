import asyncio
import sys
from logging import getLogger
from pathlib import Path

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logger = getLogger()


async def get_bot():
    from app.bot.middleware import AuthMiddleware
    from app.bot.router import bot_router
    from app.config.settings import get_settings

    settings = get_settings()
    bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp["settings"] = settings
    dp.update.outer_middleware(AuthMiddleware())
    dp.include_routers(bot_router)

    await bot.set_my_commands(
        [
            types.BotCommand(command="/start", description="Запуск бота"),
            types.BotCommand(command="/remaining", description="Посмотреть остатки"),
        ]
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    sys.path.append(str(Path().absolute()))
    logger.info("Start bot")
    asyncio.run(get_bot())
