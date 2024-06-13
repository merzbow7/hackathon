__all__ = [
    "create_app",
    "init_routers",
]

from .routes import init_routers
from .web import create_app
