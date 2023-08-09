from pathlib import Path
import aiofiles
from httpx import AsyncClient
from http import HTTPStatus

from .filetest.path_file import DOCXFILE


async def test_add_file_not_user(client: AsyncClient):
    """
    Test add file without user

    Args:
        client (AsyncClient): AsyncClient
    """

    async def file_upload(file: Path):
        async with aiofiles.open(file, "rb") as f:
            result = await f.read()

        return result

    response = await client.post(
        url="file/add?format_file=.docx",
        files={"file": ("file-sample_1MB.docx", await file_upload(DOCXFILE))},
    )

    assert response.status_code == HTTPStatus.OK
