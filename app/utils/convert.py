import os
import re
import subprocess
import tempfile

import aiofiles
from fastapi import HTTPException, status

from app.services.redis import RedisTools


class Docx2Pdf:

    def __init__(self, data: bytes, filename: str, timeout=None) -> None:
        self.data = data
        self.filename = filename
        self.timeout = timeout

    def create_tempfile(self):
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_docx:
            temp_docx.write(self.data)

        return temp_docx.name

    async def open_file(self, filename: str):
        async with aiofiles.open(filename, 'rb') as file:
            result = await file.read()

        return result

    async def convert(self) -> bytes:

        if not await RedisTools.get_pair(self.filename):

            args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', 'temp', self.create_tempfile()]

            process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=self.timeout)
            filename = re.search('-> (.*?) using filter', process.stdout.decode())

            result = await self.open_file(f'{filename.group(1)}')

            os.remove(filename.group(1))

            return result

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'A file with the same name: {self.filename} already exists'
            )