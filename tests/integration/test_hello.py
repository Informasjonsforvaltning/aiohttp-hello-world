"""Integration test cases for the root route."""
from aiohttp.test_utils import TestClient as _TestClient
import pytest


@pytest.mark.integration
async def test_hello(client: _TestClient) -> None:
    """Should return OK and given text."""
    resp = await client.get("/")
    assert resp.status == 200
    text = await resp.text()
    assert "Hello, world" in text
