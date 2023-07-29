from app.utils import AbstractRepo


class FileService:

    def __init__(self, file_repo: AbstractRepo):
        self.file_repo: AbstractRepo = file_repo()

    async def create_file(self, **kwargs):
        return await self.file_repo.add(**kwargs)
