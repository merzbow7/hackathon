from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

htmx_router = APIRouter(prefix="/web")


@htmx_router.get("/users", response_class=HTMLResponse, tags=["web-user-management"])
async def register_telegram_user(request: Request) -> HTMLResponse:
    return request.app.templates.TemplateResponse("users.html", context={"request": request})
