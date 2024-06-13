import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.db import prepare_connection, AsyncSessionMaker, make_session_factory
from app.adapters.sqlalchemy_db.users.repository import UserRepository
from app.bot import lifespan
from app.config.settings import get_settings
from app.main import init_routers
from app.main.template import prepare_template


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(lifespan=lifespan)
    app.settings = settings
    init_routers(app)
    prepare_template(app)

    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, port=80)
