import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_read_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/")
    assert response.status_code == 200
    assert "message" in response.json()

To run:
Install test dependencies (if not already installed):
pip install pytest httpx

Run Test
pytest tests/
