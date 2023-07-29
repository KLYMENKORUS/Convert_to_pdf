from app.repositories.files import FileRepository
from app.services import FileService


def file_service():
    return FileService(FileRepository)