import asyncio
from datetime import timedelta
from typing import Any
from pathlib import Path

import pytest
import aiofiles
from httpx import AsyncClient
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError, OperationalError

from app import create_app
from app.database import User, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth.hashing import Hasher
from app.utils.auth.token import Token
from app.database import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


app = create_app()

DATABASE_URL_TEST = "postgres://postgres:postgres@db_test:5432/Test_DB"

DB_CONFIG = {
    "connections": {"default": DATABASE_URL_TEST},
    "apps": {"models": {"models": ["app.database.models.models"]}},
}


@pytest.fixture(scope="session", autouse=True)
async def db() -> None:
    async def _init_db() -> None:
        await Tortoise.init(config=DB_CONFIG)
        try:
            await Tortoise._drop_databases()
        except (DBConnectionError, OperationalError):
            pass

        await Tortoise.init(config=DB_CONFIG, _create_db=True)
        await Tortoise.generate_schemas(safe=False)

    await _init_db()
    yield
    await Tortoise._drop_databases()


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": CELERY_BROKER_URL,
        "result_backend": CELERY_RESULT_BACKEND,
    }


@pytest.fixture
def celery_worker_parameters():
    """Redefine this fixture to change the init parameters of Celery workers.

    This can be used e. g. to define queues the worker will consume tasks from.

    The dict returned by your fixture will then be used
    as parameters when instantiating :class:`~celery.worker.WorkController`.
    """
    return {
        # For some reason this `celery.ping` is not registed IF our own worker is still
        # running. To avoid failing tests in that case, we disable the ping check.
        # see: https://github.com/celery/celery/issues/3642#issuecomment-369057682
        # here is the ping task: `from celery.contrib.testing.tasks import ping`
        "perform_ping_check": False,
    }


@pytest.fixture
async def create_user() -> Any:
    async def create_user(**kwargs: dict[str, Any]) -> User:
        password = kwargs.pop("password")
        hashed_password = Hasher.get_hashed_pass(password)
        kwargs.update(hashed_password=hashed_password)

        return await User.create(**kwargs)

    return create_user


@pytest.fixture
async def get_user() -> Any:
    async def get_user(**kwargs: dict[str, Any]) -> User:
        return await User.get(email=kwargs.get("email"))

    return get_user


@pytest.fixture
async def user_login() -> Any:
    async def token(**kwargs) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = Token(
            kwargs.get("email"), access_token_expires
        ).create_access_token()
        return access_token

    return token


@pytest.fixture
async def file_upload() -> Any:
    async def upload(file: Path) -> bytes:
        async with aiofiles.open(file, "rb") as f:
            result = await f.read()

            return result

    return upload
