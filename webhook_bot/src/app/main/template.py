from fastapi import FastAPI
from jinja2 import pass_context
from starlette.datastructures import URL
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


@pass_context
def https_url_for(context: dict, name: str, **path_params) -> URL:
    request = context["request"]
    http_url: URL = request.url_for(name, **path_params)
    return http_url.replace(scheme="https")


def prepare_template(app: FastAPI):
    app.templates = Jinja2Templates(directory="app/templates")
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.templates.env.globals["url_for"] = https_url_for
