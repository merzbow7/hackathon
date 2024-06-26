from fastapi import FastAPI

from app.api.root import root_router


def init_routers(app: FastAPI):
    app.include_router(root_router)
