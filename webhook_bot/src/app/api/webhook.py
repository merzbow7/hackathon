from aiogram.types import Update
from fastapi import Request
from starlette.responses import Response


async def webhook(request: Request) -> Response:
    bot = request.app.bot
    dp = request.app.dp
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return Response()
