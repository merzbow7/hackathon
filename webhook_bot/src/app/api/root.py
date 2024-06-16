from fastapi import APIRouter

from .admin.admin import admin_router
from .auth.users import auth_router

root_router = APIRouter(prefix="/api")
root_router.include_router(auth_router)
root_router.include_router(admin_router)
