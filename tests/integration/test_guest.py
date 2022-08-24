"""Integration test cases for the guests route."""
import json
from typing import Dict


from aiohttp import hdrs
from aiohttp.test_utils import TestClient as _TestClient
from multidict import MultiDict
import pytest
from pytest_mock import MockFixture

from aiohttp_hello_world.model import GuestModel

_GUEST_STORE: Dict[str, Dict] = dict(
    {
        "1": {"id": "1", "name": "First"},
        "2": {"id": "2", "name": "Second"},
    }
)


@pytest.mark.integration
async def test_guest_get_all(client: _TestClient, mocker: MockFixture) -> None:
    """Should return OK."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.get_all",
        return_value=[GuestModel.from_dict(value) for value in _GUEST_STORE.values()],
    )

    resp = await client.get("/guests")
    assert resp.status == 200
    assert resp.headers[hdrs.CONTENT_TYPE] == "application/json"

    body = await resp.json()
    with open("tests/files/expected-body-list.json", "r") as file:
        expected_body = json.load(file)

    assert body == expected_body


@pytest.mark.integration
async def test_guest_create(client: _TestClient, mocker: MockFixture) -> None:
    """Should return 201 Created, location-header and no body."""
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.add",
        return_value=str(len(_GUEST_STORE) + 1),
    )
    headers = MultiDict([(hdrs.CONTENT_TYPE, "application/json")])
    data = {"name": "Third"}

    resp = await client.post("/guests", headers=headers, json=data)

    assert resp.status == 201
    assert resp.headers[hdrs.LOCATION] == "http://localhost:8000/guests/3"

    body = await resp.read()
    assert body == b""


@pytest.mark.integration
async def test_guest_head(client: _TestClient, mocker: MockFixture) -> None:
    """Should return OK and no body."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.get",
        return_value=GuestModel.from_dict(_GUEST_STORE["1"]),
    )

    id = "1"
    resp = await client.head(f"/guests/{id}")
    assert resp.status == 200
    assert resp.headers[hdrs.CONTENT_TYPE] == "application/json"

    body = await resp.json()

    assert body is None


@pytest.mark.integration
async def test_guest_get(client: _TestClient, mocker: MockFixture) -> None:
    """Should return OK."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.get",
        return_value=GuestModel.from_dict(_GUEST_STORE["1"]),
    )

    id = "1"
    resp = await client.get(f"/guests/{id}")
    assert resp.status == 200
    assert resp.headers[hdrs.CONTENT_TYPE] == "application/json"

    body = await resp.json()
    with open("tests/files/expected-body.json", "r") as file:
        expected_body = json.load(file)

    assert body == expected_body


@pytest.mark.integration
async def test_guest_delete(client: _TestClient, mocker: MockFixture) -> None:
    """Should return 204 No content."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.get",
        return_value=GuestModel.from_dict(_GUEST_STORE["1"]),
    )
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.delete",
        return_value=True,
    )

    id = "1"
    resp = await client.delete(f"/guests/{id}")
    assert resp.status == 204


# Bad cases


@pytest.mark.integration
async def test_guest_create_without_mandatory_attribute(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 422 Unprocessable Entity and message in body."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.add",
        return_value=None,
    )

    headers = MultiDict([(hdrs.CONTENT_TYPE, "application/json")])
    data = {"adress": "Third"}

    resp = await client.post("/guests", headers=headers, json=data)

    assert resp.status == 422
    assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]

    body = await resp.json()
    assert body["detail"] == "Mandatory property name is missing."


@pytest.mark.integration
async def test_guest_create_adapter_returns_none(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 400 Bad request and message in body."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.add",
        return_value=None,
    )

    headers = MultiDict([(hdrs.CONTENT_TYPE, "application/json")])
    data = {"name": "Third"}

    resp = await client.post("/guests", headers=headers, json=data)

    assert resp.status == 400
    assert "application/json" in resp.headers[hdrs.CONTENT_TYPE]

    body = await resp.json()
    assert body["detail"] == "Could not create hello_world."


@pytest.mark.integration
async def test_guest_get_when_not_found(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 404 Not Found."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.get",
        return_value=None,
    )

    id = "does_not_exist"
    resp = await client.get(f"/guests/{id}")
    assert resp.status == 404


@pytest.mark.integration
async def test_guest_head_when_not_found(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 404 Not Found."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.get",
        return_value=None,
    )

    id = "does_not_exist"
    resp = await client.head(f"/guests/{id}")
    assert resp.status == 404


@pytest.mark.integration
async def test_guest_delete_when_not_found(
    client: _TestClient, mocker: MockFixture
) -> None:
    """Should return 404 Not found."""
    # Patch the store:
    mocker.patch(
        "aiohttp_hello_world.adapter.FakeRepository.delete",
        return_value=False,
    )

    id = "does_not_exist"
    resp = await client.delete(f"/guests/{id}")
    assert resp.status == 404
