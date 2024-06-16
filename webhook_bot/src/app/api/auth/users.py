import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response

from app.adapters.sqlalchemy_db.users.repository import get_user_repo
from app.main.auth import KcUser, get_user_info

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/registration")
async def register_telegram_user(
    kc_user: Annotated[KcUser, Depends(get_user_info)],
    code: uuid.UUID,
):
    repo = get_user_repo()
    user = await repo.verify(code, kc_user.id)
    if not user:
        raise HTTPException(status_code=400, detail="Ошибка авторизации")
    return Response(status_code=200)
