import uvicorn
from fastapi import FastAPI

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
