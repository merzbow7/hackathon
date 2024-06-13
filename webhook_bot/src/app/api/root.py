from fastapi import APIRouter

from .admin.admin import admin_router
from .admin.html import htmx_router
from .auth.users import auth_router

root_router = APIRouter(prefix="/api")
root_router.include_router(auth_router)
root_router.include_router(admin_router)

web_router = APIRouter()
web_router.include_router(htmx_router)
