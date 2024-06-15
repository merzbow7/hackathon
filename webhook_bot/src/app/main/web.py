import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.main import init_routers
from app.main.template import prepare_template


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI()
    app.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routers(app)
    prepare_template(app)

    return app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, port=80)
