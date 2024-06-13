from typing import TypeAlias

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config.settings import get_settings
from app.main.typed import FastApiApp

AsyncSessionMaker: TypeAlias = async_sessionmaker

settings = get_settings()
engine = create_async_engine(settings.db_uri.unicode_string(), echo=True)


def make_session_factory() -> AsyncSessionMaker:
    return async_sessionmaker(engine, expire_on_commit=False)


def prepare_connection(app: FastApiApp):
    app.async_session = make_session_factory()
