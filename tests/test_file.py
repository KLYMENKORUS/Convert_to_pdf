from pathlib import Path
from typing import Any, Callable
from itertools import dropwhile

from httpx import AsyncClient
from http import HTTPStatus
from celery.result import AsyncResult

from .filetest.path_file import DOCX_FILE_PATH, DOCX_FILE
from app.database import User
from app.services.redis import RedisTools


async def test_add_file_not_user(
    client: AsyncClient, file_upload: Callable[[Path], bytes]
):
    """
    Test add file without user

    Args:
        client (AsyncClient): AsyncClient
        file_upload (Callable[[Path], bytes]): fixture file upload
    """

    response = await client.post(
        url="file/add",
        params={"format_file": ".docx"},
        files={"file": (DOCX_FILE, await file_upload(DOCX_FILE_PATH))},
    )

    assert response.status_code == HTTPStatus.OK, response.text


async def test_add_file_user(
    client: AsyncClient,
    create_user: Callable[[dict[str, str]], User],
    file_upload: Callable[[Path], bytes],
):
    """
    Test add file by user

    Args:
        client (AsyncClient): AsyncClient
        create_user (Callable[[dict[str, str]], User]): fixture create user
        file_upload (Callable[[Path], bytes]): fixture file upload
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
        files={"file": (DOCX_FILE, await file_upload(DOCX_FILE_PATH))},
    )
    response_failed = await client.post(
        url="file/add",
        params={"format_file": ".jpg", "username": user.email},
        files={"file": (DOCX_FILE, await file_upload(DOCX_FILE_PATH))},
    )

    assert response.status_code == HTTPStatus.OK
    assert response_failed.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_file_get_user(
    client: AsyncClient,
    get_user: Callable[[dict[str, Any]], User],
):
    """
    Test file get method by user

    Args:
        client (AsyncClient): AsyncClient
        get_user (Callable[[dict[str, Any]], User]): pytest fixtures
    """

    list_tasks = await RedisTools.task_celery()

    for _ in dropwhile(
        lambda task: AsyncResult(task.split(b"-", 3)[-1]).status == "PENDING",
        list_tasks,
    ):
        user = await get_user(email="user@example.com")
        response = await client.get(
            url="file/get",
            params={
                "filename": DOCX_FILE.split(".")[0],
                "username": user.email,
            },
        )
        response_failed = await client.get(
            url="file/get",
            params={"filename": "file-sample", "username": user.email},
        )
        assert response.status_code == HTTPStatus.OK, response.text
        assert response_failed.status_code == HTTPStatus.NOT_FOUND


async def test_file_get_not_user(client: AsyncClient):
    """
    Test file get method not user

    Args:
        client (AsyncClient): AsyncClient
    """

    list_tasks = await RedisTools.task_celery()

    for _ in dropwhile(
        lambda task: AsyncResult(task.split(b"-", 3)[-1]).status == "PENDING",
        list_tasks,
    ):
        response = await client.get(
            url="file/get",
            params={
                "filename": DOCX_FILE.split(".")[0],
            },
        )
        response_failed = await client.get(
            url="file/get",
            params={"filename": "file-sample"},
        )
        assert response.status_code == HTTPStatus.OK, response.text
        assert response_failed.status_code == HTTPStatus.NOT_FOUND


async def test_all_file_by_user(
    client: AsyncClient,
    get_user: Callable[[dict[str, Any]], User],
    user_login: Callable[[str], str],
):
    """
    Test all files by user

    Args:
        client (AsyncClient): AsyncClient
        get_user (Callable[[dict[str, Any]], User]): pytest fixtures
        user_login (Callable[[str], str]): pytest fixtures
    """

    list_tasks = await RedisTools.task_celery()

    for _ in dropwhile(
        lambda task: AsyncResult(task.split(b"-", 3)[-1]).status == "PENDING",
        list_tasks,
    ):
        user = await get_user(email="user@example.com")
        token = await user_login(email=user.email)

        response = await client.get(
            url="file/all", headers={"Authorization": "Bearer " + token}
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]["user_email"] == user.email


async def test_file_delete_by_user(
    client: AsyncClient,
    get_user: Callable[[dict[str, Any]], User],
    user_login: Callable[[str], str],
):
    """
    Delete a by user the file

    Args:
        client (AsyncClient): AsyncClient
        get_user (Callable[[dict[str, Any]], User]): pytest fixtures
        user_login (Callable[[str], str]): pytest fixtures
    """
    list_tasks = await RedisTools.task_celery()

    for _ in dropwhile(
        lambda task: AsyncResult(task.split(b"-", 3)[-1]).status == "PENDING",
        list_tasks,
    ):
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

        assert response.status_code == HTTPStatus.OK, response.text
        assert response_failed.status_code == HTTPStatus.NOT_FOUND
