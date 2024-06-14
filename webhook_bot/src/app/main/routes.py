from app.api.root import root_router, web_router
from app.api.webhook import webhook
from app.main.typed import FastApiApp


def init_routers(app: FastApiApp):
    app.include_router(root_router)
    app.include_router(web_router)

    webhook_endpoint = f"/webhook/{app.settings.webhook_part}"
    app.add_route(webhook_endpoint, webhook, ["post"], include_in_schema=False)
