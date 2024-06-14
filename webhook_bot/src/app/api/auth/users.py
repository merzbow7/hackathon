import uuid

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.adapters.sqlalchemy_db.users.repository import get_user_repo
from app.bot.commands.start import enjoy_bot

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/registration", response_class=HTMLResponse)
async def register_telegram_user(
    request: Request,
    code: uuid.UUID,
) -> dict:
    repo = get_user_repo()
    user = await repo.verify(code)
    print(f"{user=}")
    if user:
        await enjoy_bot(request.app.bot, user.telegram_id)

    return request.app.templates.TemplateResponse("auth.html", context={"request": request, "user": user})
