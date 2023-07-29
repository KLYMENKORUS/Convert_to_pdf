from fastapi import FastAPI
from app.configuration.server import Server


def create_app(_=None) -> FastAPI:
    """Create app FastAPI"""

    app = FastAPI()

    return Server(app).get_app()