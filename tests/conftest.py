import asyncio
import sys

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.testclient import TestClient

from db.models.base import DBBase
from settings import settings
from main import app


@pytest.fixture(scope="session")
def fake():
    return Faker()


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _database_url():
    return settings.get_db_url()


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(
        settings.get_db_url()
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(scope="session")
async def init_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(DBBase.metadata.create_all)
    return DBBase.metadata.create_all


@pytest.fixture()
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(DBBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(DBBase.metadata.drop_all)


@pytest.fixture
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture
def test_app(session):
    with TestClient(app) as client:
        yield client
