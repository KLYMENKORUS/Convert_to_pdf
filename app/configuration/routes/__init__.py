from .routes import Routes
from app.internal import user_router

__routes__ = Routes((user_router,))