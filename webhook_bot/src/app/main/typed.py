from typing import TypeVar, TYPE_CHECKING
from fastapi import FastAPI
from starlette.templating import Jinja2Templates

if TYPE_CHECKING:
    from app.config.settings import Settings
    from aiogram import Dispatcher, Bot


class FastApp:
    db: "Dispatcher"
    bot: "Bot"
    settings: "Settings"
    templates: Jinja2Templates


FastApiApp = TypeVar("FastApiApp", FastAPI, FastApp)
