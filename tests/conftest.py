import asyncio
import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from app import create_app


app = create_app()

DATABASE_URL_TEST = (
    "postgres://postgres_test:postgres_test@127.0.0.1:5436/Testdb"
)

DB_CONFIG = {
    "connections": {"default": DATABASE_URL_TEST},
    "apps": {"models": {"models": ["app.database.models.models"]}},
}


async def init_db(
    db_url, create_db: bool = False, schemas: bool = False
) -> None:
    """Initial database connection"""
    await Tortoise.init(config=DB_CONFIG, _create_db=create_db)
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DATABASE_URL_TEST):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
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
