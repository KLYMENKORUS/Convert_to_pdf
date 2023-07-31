from functools import wraps
from typing import ParamSpec, TypeVar, Callable, Awaitable

from fastapi import HTTPException, status

from app.services.redis import RedisTools
from .convert import Docx2Pdf


P = ParamSpec("P")
R = TypeVar("R")

REDIS_MESSAGE = 'There is no file named in temporary storage'
DB_MESSAGE = 'File with given name does not exist'


class Convert:

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            pdf = await Docx2Pdf(
                await kwargs.get('data_file').read(),
                kwargs.get('filename')
            ).convert()

            kwargs.update(data_file=pdf)

            return await func(*args, **kwargs)

        return wrapper


class DoesntNotExists:

    def __init__(self, action: str) -> None:
        self.action = action
        self.message_redis = REDIS_MESSAGE
        self.message_db = DB_MESSAGE
        self.exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.message_redis if action == 'redis' else self.message_db
        )

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            match self.action:
                case 'redis':
                    file_data = await RedisTools.get_pair(kwargs.get('filename'))

                    if file_data:
                        kwargs.update(file_data=file_data)
                        return await func(*args, **kwargs)
                    else:
                        raise self.exception

        return wrapper
