from pathlib import Path
import aiofiles
from httpx import AsyncClient
from http import HTTPStatus

from .filetest.path_file import DOCXFILE


async def test_create_user(client: AsyncClient):
    """
    Test create_user

    Args:
        client (AsyncClient): AsyncClient
    """
    user = {
        "username": "string",
        "email": "user@example.com",
        "password": "string",
    }

    response = await client.post(url="user/register", json=user)
    assert response.status_code == HTTPStatus.OK


async def test_login_user(client: AsyncClient):
    """
    Test login

    Args:
        client (AsyncClient): AsyncClient
    """

    response = await client.post(
        url="user/login",
        data={"username": "user@example.com", "password": "string"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


async def test_login_failed_username(client: AsyncClient):
    """
    Test login failed

    Args:
        client (AsyncClient): AsyncClient
    """
    response = await client.post(
        url="user/login",
        data={"username": "user@examples.com", "password": "string"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_login_failed_password(client: AsyncClient):
    """
    Test login failed

    Args:
        client (AsyncClient): AsyncClient
    """
    response = await client.post(
        url="user/login",
        data={"username": "user@example.com", "password": "12345"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
