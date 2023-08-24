from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.services.redis import RedisTools
from app.repositories.files import FileRepository
from app.worker.tasks import convert_file, jpg2pdf


@dataclass(slots=True)
class Convert:
    file_repo = FileRepository()
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"A file with the same name already exists",
    )

    async def __call__(self, **kwargs: Any) -> Any:
        match kwargs.get("action"):
            case "redis":
                if not await RedisTools.get_pair(kwargs.get("filename")):
                    return self.filter_format_file(
                        kwargs.get("format_file"), kwargs.get("data")
                    )
                else:
                    raise self.exception
            case "db":
                try:
                    if await self.file_repo.get(
                        "file_name", kwargs.get("filename")
                    ):
                        raise self.exception
                except (DoesNotExist, IntegrityError):
                    return self.filter_format_file(
                        kwargs.get("format_file"), kwargs.get("data")
                    )

    def filter_format_file(self, format_file: str, data: bytes) -> Any:
        match format_file:
            case ".docx":
                result = convert_file.delay(data)
            case ".jpg":
                result = jpg2pdf.delay(data)

        return result
