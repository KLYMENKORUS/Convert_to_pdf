from .routes import Routes
from app.internal import user_router
from app.internal import files_router

__routes__ = Routes((user_router, files_router))