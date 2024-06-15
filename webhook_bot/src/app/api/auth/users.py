import uuid

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.adapters.sqlalchemy_db.users.repository import get_user_repo

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/registration", response_class=HTMLResponse)
async def register_telegram_user(
    request: Request,
    code: uuid.UUID,
) -> dict:
    repo = get_user_repo()
    user = await repo.verify(code)

    return request.app.templates.TemplateResponse("auth.html", context={"request": request, "user": user})
