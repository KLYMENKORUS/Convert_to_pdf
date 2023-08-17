from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.services.redis import RedisTools
from app.repositories.files import FileRepository
from app.worker.tasks import convert_file
from app.utils.docx2pdf import Docx2Pdf


@dataclass(slots=True)
class Convert:
    doc2pdf = Docx2Pdf()
    file_repo = FileRepository()
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"A file with the same name already exists",
    )

    async def __call__(self, **kwargs: Any) -> Any:
        match kwargs.get("action"):
            case "redis":
                if not await RedisTools.get_pair(kwargs.get("filename")):
                    return convert_file.delay(data=kwargs.get("data"))

                else:
                    raise self.exception
            case "db":
                try:
                    if await self.file_repo.get(
                        file_name=kwargs.get("filename")
                    ):
                        raise self.exception
                except (DoesNotExist, IntegrityError):
                    return convert_file.delay(data=kwargs.get("data"))
