from dataclasses import dataclass
from typing import Annotated, Any, Type

from fastapi import Depends


from app.repositories.files import FileRepository
from app.services import FileService, FileServiceRedis
from app.utils.format_file import Cyrillic


@dataclass(slots=True)
class OperationFiles:
    file_serv = FileService(FileRepository)
    redis_serv = FileServiceRedis()

    @classmethod
    async def add_operation(cls, **kwargs) -> Any:
        if kwargs.get("email") is None:
            await cls.redis_serv.write_to_redis(**kwargs)
        else:
            await cls.file_serv.create_file(**kwargs)

    @classmethod
    async def get_operation(cls, **kwargs) -> bytes:
        if kwargs.get("email") is None:
            return await cls.redis_serv.get_file_redis(**kwargs)
        else:
            return await cls.file_serv.get_file_db(**kwargs)

    @classmethod
    async def all_operation(cls, **kwargs: Any) -> Any:
        return await cls.file_serv.all_files_by_user(**kwargs)

    @classmethod
    async def file_delete(cls, **kwargs: Any) -> None:
        await cls.file_serv.file_delete(**kwargs)


def cyrillic() -> Type[Cyrillic]:
    return Cyrillic()


file_services = Annotated[OperationFiles, Depends(OperationFiles)]
