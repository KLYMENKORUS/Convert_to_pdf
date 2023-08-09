from httpx import AsyncClient
from http import HTTPStatus


async def test_create_user(client: AsyncClient):
    new_user = {
        "username": "string",
        "email": "user@example.com",
        "password": "string",
    }

    response = await client.post(url="user/register", data=new_user)

    assert response.status_code == HTTPStatus.OK
