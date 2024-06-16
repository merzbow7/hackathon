from aiogram import Router

from app.bot.commands.remaining import remaining_router
from app.bot.commands.start import start_router

bot_router = Router()
bot_router.include_routers(start_router, remaining_router)
