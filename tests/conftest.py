import pytest
from httpx import AsyncClient

from src.app.configurator.containers import Container
from src.app.main import app


@pytest.fixture
def container():
    return Container()


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def anyio_backend():
    return "asyncio"
