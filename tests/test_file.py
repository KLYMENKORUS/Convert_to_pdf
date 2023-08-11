from pathlib import Path

import aiofiles
from httpx import AsyncClient
from http import HTTPStatus

from .filetest.path_file import DOCXFILE


async def file_upload(file: Path):
    async with aiofiles.open(file, "rb") as f:
        result = await f.read()

    return result


async def test_add_file_not_user(client: AsyncClient):
    """
    Test add file without user

    Args:
        client (AsyncClient): AsyncClient
    """

    response = await client.post(
        url="file/add",
        params={"format_file": ".docx"},
        files={"file": ("file-sample_1MB.docx", await file_upload(DOCXFILE))},
    )

    assert response.status_code == HTTPStatus.OK


async def test_add_file_user(client: AsyncClient, create_user):
    """
    Test add file by user

    Args:
        client (AsyncClient): AsyncClient
    """
    user = await create_user(
        **{
            "username": "string",
            "email": "user@example.com",
            "password": "string",
        }
    )
    response = await client.post(
        url="file/add",
        params={"format_file": ".docx", "username": user.email},
        files={"file": ("file-sample_1MB.docx", await file_upload(DOCXFILE))},
    )
    response_failed = await client.post(
        url="file/add",
        params={"format_file": ".doc", "username": user.email},
        files={"file": ("file-sample_1MB.docx", await file_upload(DOCXFILE))},
    )

    assert response.status_code == HTTPStatus.OK
    assert response_failed.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_file_get(client: AsyncClient, get_user):
    """
    Test file get method

    Args:
        client (AsyncClient): AsyncClient
        get_user (function): pytest fixtures
    """
    user = await get_user(email="user@example.com")
    response = await client.get(
        url="file/get",
        params={"filename": "file-sample_1MB", "username": user.email},
    )
    response_failed = await client.get(
        url="file/get",
        params={"filename": "file-sample", "username": user.email},
    )
    assert response.status_code == HTTPStatus.OK
    assert response_failed.status_code == HTTPStatus.NOT_FOUND


async def test_all_file_by_user(client: AsyncClient, get_user, user_login):
    """
    Test all files by user

    Args:
        client (AsyncClient): AsyncClient
        get_user (function): pytest fixtures
        user_login (function): pytest fixtures
    """
    user = await get_user(email="user@example.com")
    token = await user_login(email=user.email)

    response = await client.get(
        url="file/all", headers={"Authorization": "Bearer " + token}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()[0]["user_email"] == user.email


async def test_file_delete_by_user(client: AsyncClient, get_user, user_login):
    """_summary_

    Args:
        client (AsyncClient): AsyncClient
        get_user (function): pytest fixtures
        user_login (function): pytest fixtures
    """
    user = await get_user(email="user@example.com")
    token = await user_login(email=user.email)

    response = await client.delete(
        url="file/delete",
        headers={"Authorization": "Bearer " + token},
        params={"filename": "file-sample_1MB"},
    )
    response_failed = await client.delete(
        url="file/delete",
        headers={"Authorization": "Bearer " + token},
        params={"filename": "file-sample_1MB"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response_failed.status_code == HTTPStatus.NOT_FOUND
