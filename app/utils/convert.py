import os
import re
import subprocess
import tempfile
from dataclasses import dataclass

import aiofiles
from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist, IntegrityError

from app.services.redis import RedisTools
from app.repositories.files import FileRepository


@dataclass(frozen=True, slots=True)
class Docx2Pdf:
    timeout = None
    file_repo = FileRepository()
    exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"A file with the same name already exists",
    )

    def create_tempfile(self, data: bytes):
        with tempfile.NamedTemporaryFile(
            suffix=".docx", delete=False
        ) as temp_docx:
            temp_docx.write(data)

        return temp_docx.name

    async def open_file(self, filename: str):
        async with aiofiles.open(filename, "rb") as file:
            result = await file.read()

        return result

    async def convert(self, **kwargs) -> bytes:
        args = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            "temp",
            self.create_tempfile(kwargs.get("data")),
        ]

        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=self.timeout,
        )
        filename = re.search("-> (.*?) using filter", process.stdout.decode())

        result = await self.open_file(f"{filename.group(1)}")

        os.remove(filename.group(1))

        return result

    async def adjacent_convert(self, **kwargs):
        match kwargs.get("action"):
            case "redis":
                if not await RedisTools.get_pair(kwargs.get("filename")):
                    return await self.convert(data=kwargs.get("data"))

                else:
                    raise self.exception
            case "db":
                try:
                    if await self.file_repo.get(
                        file_name=kwargs.get("filename")
                    ):
                        raise self.exception
                except (DoesNotExist, IntegrityError):
                    return await self.convert(data=kwargs.get("data"))
