from httpx import AsyncClient
from http import HTTPStatus


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
