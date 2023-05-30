import pytest
from httpx import AsyncClient

from asdf.main import app


@pytest.mark.asyncio
async def test_get_root() -> None:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


@pytest.mark.asyncio
async def test_get_one() -> None:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/1/")

    assert response.status_code == 200
    assert response.json() == {"num_of_items": 28066}
