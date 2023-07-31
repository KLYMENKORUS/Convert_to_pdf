from app.utils import AbstractRepo
from app.utils.wrapper import Convert, DoesntNotExists

from .redis import RedisTools


class FileService:

    def __init__(self, file_repo: AbstractRepo):
        self.file_repo: AbstractRepo = file_repo()

    @Convert()
    async def create_file(self, **kwargs):
        return await self.file_repo.add(**kwargs)


class FileServiceRedis:

    @Convert()
    async def write_to_redis(self, **kwargs):
        return await RedisTools.set_pair(
            kwargs.get('filename'), kwargs.get('data_file')
        )

    @DoesntNotExists('redis')
    async def get_file_redis(self, **kwargs):
        return kwargs.get('file_data')

