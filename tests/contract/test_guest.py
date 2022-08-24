"""Contract test cases for ready."""
import json
from typing import Any

from aiohttp import ClientSession, hdrs
import pytest


@pytest.mark.contract
@pytest.mark.asyncio
async def test_hello_world_post(http_service: Any) -> None:
    """Should return 201 Created and location header."""
    url = f"{http_service}/guests"

    headers = {hdrs.CONTENT_TYPE: "application/json"}
    with open("tests/files/new-body.json", "r") as f:
        data = json.load(f)

    session = ClientSession()
    async with session.post(url, headers=headers, json=data) as resp:
        pass
    await session.close()

    assert resp.status == 201

    # Check the location header
    assert resp.headers[hdrs.LOCATION]
    session = ClientSession()
    async with session.head(resp.headers[hdrs.LOCATION]) as resp:
        pass
    await session.close()
    assert resp.status == 200


@pytest.mark.contract
@pytest.mark.asyncio
async def test_hello_world_head(http_service: Any) -> None:
    """Should return 200 OK."""
    url = f"{http_service}/guests/1"

    session = ClientSession()
    async with session.head(url) as resp:
        pass
    await session.close()

    assert resp.status == 200


@pytest.mark.contract
@pytest.mark.asyncio
async def test_hello_world_get(http_service: Any) -> None:
    """Should return 200 OK."""
    url = f"{http_service}/guests/1"

    session = ClientSession()
    async with session.get(url) as resp:
        pass
    await session.close()

    assert resp.status == 200


@pytest.mark.contract
@pytest.mark.asyncio
async def test_hello_world_delete(http_service: Any) -> None:
    """Should return status 404."""
    url = f"{http_service}/guests/1"

    session = ClientSession()
    async with session.delete(url) as resp:
        assert resp.status == 204

    async with session.get(url) as resp:
        assert resp.status == 404
    await session.close()
