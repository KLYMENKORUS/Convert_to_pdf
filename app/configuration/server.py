from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.configuration.routes import __routes__
from app.database import DB_CONFIG


class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_table(app)
        self.__register_routes(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_table(app):
        register_tortoise(
            app=app,
            config=DB_CONFIG,
            generate_schemas=False
        )

    @staticmethod
    def __register_routes(app):
        __routes__.register_routes(app)
