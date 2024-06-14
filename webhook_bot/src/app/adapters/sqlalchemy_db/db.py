from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config.settings import get_settings

settings = get_settings()
engine = create_async_engine(settings.db_uri.unicode_string(), echo=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


def get_session() -> Generator[AsyncSession, None, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
