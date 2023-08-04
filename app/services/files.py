from app.utils import AbstractRepo
from app.utils.wrapper import Convert, DoesntNotExists
from app.utils.auth.decorator import CheckUser

from .redis import RedisTools


class FileService:

    def __init__(self, file_repo: AbstractRepo):
        self.file_repo: AbstractRepo = file_repo()

    @Convert('db')
    @CheckUser()
    async def create_file(self, **kwargs):
        return await self.file_repo.add(**kwargs)
    
    @CheckUser()
    @DoesntNotExists('db')
    async def get_file_db(self, **kwargs):
        file = await self.file_repo.get(file_name=kwargs.get('file_name'))
        return file.data_file


class FileServiceRedis:

    @Convert('redis')
    async def write_to_redis(self, **kwargs):
        return await RedisTools.set_pair(
            kwargs.get('filename'), kwargs.get('data_file')
        )

    @DoesntNotExists('redis')
    async def get_file_redis(self, **kwargs):
        return kwargs.get('file_data')

