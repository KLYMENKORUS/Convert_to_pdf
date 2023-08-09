from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.configuration.routes import __routes__
from app.database import DB_CONFIG
from app.services.redis import RedisTools
from app.utils.wrapper import RepeatEvery


class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_table(app)
        self.__register_events(app)
        self.__register_routes(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_table(app: FastAPI):
        register_tortoise(
            app=app,
            config=DB_CONFIG,
            generate_schemas=False
        )
    
    @staticmethod
    def __register_events(app: FastAPI):

        @app.on_event('startup')
        @RepeatEvery(seconds=60*5)
        async def on_startup():
            await RedisTools.flush()


    @staticmethod
    def __register_routes(app: FastAPI):
        __routes__.register_routes(app)
