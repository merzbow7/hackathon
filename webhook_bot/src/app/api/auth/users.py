import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.adapters.sqlalchemy_db.db import AsyncSessionMaker, make_session_factory
from app.adapters.sqlalchemy_db.users.repository import UserRepository
from app.bot.commands.start import enjoy_bot

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/registration", response_class=HTMLResponse)
async def register_telegram_user(
    request: Request,
    code: uuid.UUID,
    session_maker: Annotated[AsyncSessionMaker, Depends(make_session_factory)],
) -> dict:
    repo = UserRepository(session_maker)
    user = await repo.verify(code)
    if user:
        await enjoy_bot(request.app.bot, user.telegram_id)

    return request.app.templates.TemplateResponse("auth.html", context={"request": request, "user": user})
