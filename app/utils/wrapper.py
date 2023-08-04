from functools import wraps
from typing import ParamSpec, TypeVar, Callable, Awaitable

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.services.redis import RedisTools
from app.utils.convert import Docx2Pdf
from app.repositories.files import FileRepository


P = ParamSpec("P")
R = TypeVar("R")

REDIS_MESSAGE = 'There is no file named in temporary storage'
DB_MESSAGE = 'File with given name does not exist'


class Convert:

    def __init__(self, action: str) -> None:
        self.action = action
        self.docx2pdf = Docx2Pdf()

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            pdf = await self.docx2pdf.adjacent_convert(
                action=self.action,
                filename=kwargs.get('filename'),
                data=await kwargs.get('data_file').read()
            )

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
        self.file_repo = FileRepository()

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            match self.action:
                case 'redis':
                    if file_data := await RedisTools.get_pair(kwargs.get('filename')):
                        kwargs.update(file_data=file_data)
                        return await func(*args, **kwargs)
                    else:
                        raise self.exception
                
                case 'db':
                    try:
                        if await self.file_repo.get(file_name=kwargs.get('file_name')):
                            return await func(*args, **kwargs)
                        
                    except DoesNotExist:
                        raise self.exception

        return wrapper