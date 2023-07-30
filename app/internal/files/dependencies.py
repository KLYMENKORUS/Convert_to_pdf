from app.repositories.files import FileRepository
from app.services import FileService, FileServiceRedis


def file_service():
    return FileService(FileRepository)


def redis_service():
    return FileServiceRedis()
