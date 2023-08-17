import logging
from typing import Any, Optional

from celery.result import AsyncResult

from app.utils import AbstractRepo
from app.utils.wrapper import Convert, DoesntNotExists, TasksCelery
from app.utils.auth.decorator import CheckUser

from .redis import RedisTools


logger = logging.getLogger(__name__)


class FileService:
    dict_file: dict[str, Any] = dict()
    func_create: Optional[AbstractRepo] = None

    def __init__(self, file_repo: AbstractRepo):
        self.file_repo: AbstractRepo = file_repo()

    @Convert("db")
    @CheckUser()
    async def create_file(self, **kwargs: Any) -> dict[str, Any]:
        FileService.dict_file = dict(
            user=kwargs.get("user"),
            file_name=kwargs.get("filename").split(".")[0],
            data_file=kwargs.get("result"),
        )
        FileService.func_create = self.file_repo.add
        return

    @classmethod
    @TasksCelery()
    async def to_database(cls, **kwargs: Any):
        file: AsyncResult = kwargs.get("file")

        if file.status == "SUCCESS" and file is not None:
            cls.dict_file.update(data_file=file.result)
            await cls.func_create(**cls.dict_file)
            logger.info("Successfully file added to Database")

            await RedisTools.delete_key(*kwargs.get("files"))
            logger.info("Successfully deleted")

    @CheckUser()
    @DoesntNotExists("db")
    async def get_file_db(self, **kwargs: Any) -> bytes:
        file = await self.file_repo.get(file_name=kwargs.get("filename"))
        return file.data_file

    async def all_files_by_user(self, **kwargs: Any) -> Any:
        return await self.file_repo.all_by_filter(**kwargs)

    @DoesntNotExists("db")
    async def file_delete(self, **kwargs: Any) -> None:
        await self.file_repo.delete(**kwargs)


class FileServiceRedis:
    filename: Optional[str] = None

    @Convert("redis")
    async def write_to_redis(self, **kwargs: Any) -> None:
        FileServiceRedis.filename = kwargs.get("filename").split(".")[0]

        return

    @classmethod
    @TasksCelery()
    async def to_redis(cls, **kwargs: Any):
        file: AsyncResult = kwargs.get("file")

        if file.status == "SUCCESS" and file is not None:
            await RedisTools.set_pair(cls.filename, file.result)
            logger.info("Successfully file added to Redis")

            await RedisTools.delete_key(*kwargs.get("files"))
            logger.info("Successfully deleted")

    @DoesntNotExists("redis")
    async def get_file_redis(self, **kwargs: Any) -> bytes:
        return kwargs.get("file_data")
