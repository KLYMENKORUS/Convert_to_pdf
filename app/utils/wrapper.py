import asyncio
from dataclasses import dataclass
from functools import wraps
from typing import ParamSpec, TypeVar, Callable, Awaitable

from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from tortoise.exceptions import DoesNotExist
from celery.result import AsyncResult

from app.services.redis import RedisTools
from app.utils.convert import Convert
from app.repositories.files import FileRepository


P = ParamSpec("P")
R = TypeVar("R")

REDIS_MESSAGE = "There is no file named in temporary storage"
DB_MESSAGE = "File with given name does not exist"


@dataclass(frozen=True, slots=True)
class Convert:
    action: str
    convert = Convert()
    wrong_format = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Wrong file format",
    )

    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            if (
                kwargs.get("format_file") == ".docx"
                and kwargs.get("filename").split(".")[1] == "docx"
            ) or (
                kwargs.get("format_file") == ".jpg"
                and kwargs.get("filename").split(".")[1] == "jpg"
            ):
                pdf = await self.convert(
                    action=self.action,
                    filename=kwargs.get("filename").split(".")[0],
                    data=await kwargs.get("data_file").read(),
                    format_file=kwargs.get("format_file"),
                )

                kwargs.update(result=pdf)
                kwargs.pop("format_file")

                return await func(*args, **kwargs)
            else:
                raise self.wrong_format

        return wrapper


@dataclass(frozen=True, slots=True)
class DoesntNotExists:
    action: str = "db"
    message_redis = REDIS_MESSAGE
    message_db = DB_MESSAGE
    exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=message_redis if action == "redis" else message_db,
    )
    file_repo = FileRepository()

    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            match self.action:
                case "redis":
                    if file_data := await RedisTools.get_pair(
                        kwargs.get("filename")
                    ):
                        kwargs.update(file_data=file_data)
                        return await func(*args, **kwargs)
                    else:
                        raise self.exception

                case "db":
                    try:
                        if await self.file_repo.get(
                            file_name=kwargs.get("filename")
                        ):
                            return await func(*args, **kwargs)

                    except DoesNotExist:
                        raise self.exception

        return wrapper


@dataclass(frozen=True, slots=True)
class RepeatEvery:
    seconds: float | int

    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper():
            is_coroutine = asyncio.iscoroutinefunction(func)

            async def loop():
                while True:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                    except Exception as e:
                        print(e)
                    await asyncio.sleep(self.seconds)

            asyncio.create_task(loop())

        return wrapper


@dataclass(slots=True)
class TasksCelery:
    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            if files := await RedisTools.task_celery():
                file_id = files[0].split(b"-", 3)[-1]
                file = AsyncResult(file_id)

                kwargs.setdefault("file", file)
                kwargs.setdefault("files", files)

                return await func(*args, **kwargs)

        return wrapper
