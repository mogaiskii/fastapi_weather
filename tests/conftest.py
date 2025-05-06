import asyncio
import json
import sys

import pytest
from faker import Faker
from starlette.testclient import TestClient

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


@pytest.fixture
def test_app():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def load_test_json_data():
    def load_data(file_name):
        with open("tests/data/" + file_name) as data_file:
            return json.load(data_file)
    return load_data
