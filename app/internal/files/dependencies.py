from dataclasses import dataclass
from typing import Any


from app.repositories.files import FileRepository
from app.services import FileService, FileServiceRedis



@dataclass(slots=True)
class OperationFiles:

    file_serv = FileService(FileRepository)
    redis_serv = FileServiceRedis()

    @classmethod
    async def add_operation(cls, **kwargs) -> Any:
        if kwargs.get('email') is None:
            await cls.redis_serv.write_to_redis(**kwargs)
        else:
            await cls.file_serv.create_file(**kwargs)
    
    @classmethod
    async def get_operation(cls, **kwargs) -> bytes:
        if kwargs.get('email') is None:
            return await cls.redis_serv.get_file_redis(**kwargs)
        else:
            return await cls.file_serv.get_file_db(**kwargs)