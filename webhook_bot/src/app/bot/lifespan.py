from contextlib import asynccontextmanager
from urllib.parse import urljoin

from app.bot.main import get_bot
from app.config.settings import get_settings
from app.main.typed import FastApiApp


@asynccontextmanager
async def lifespan(app: FastApiApp):
    dp, bot = await get_bot(app)
    settings = get_settings()
    dp["settings"] = settings
    dp["app"] = app

    webhook_endpoint = f"/webhook/{settings.webhook_part}"
    webhook_url = urljoin(settings.base_url, webhook_endpoint)

    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != webhook_url:
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
    yield
