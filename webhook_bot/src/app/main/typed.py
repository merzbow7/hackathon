from typing import TYPE_CHECKING, TypeVar

from fastapi import FastAPI
from starlette.templating import Jinja2Templates

if TYPE_CHECKING:
    from aiogram import Bot, Dispatcher

    from app.config.settings import Settings


class FastApp:
    db: "Dispatcher"
    bot: "Bot"
    settings: "Settings"
    templates: Jinja2Templates


FastApiApp = TypeVar("FastApiApp", FastAPI, FastApp)
