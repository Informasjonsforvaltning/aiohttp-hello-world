"""Integration test cases for the hello_world graph adapter."""
from typing import Any, Dict

import pytest

from aiohttp_hello_world.adapter import FakeRepository
from aiohttp_hello_world.model import GuestModel
from aiohttp_hello_world.service import GuestService

# Set up a fake repository for testing.
_TEST_DB: Dict[str, Dict] = dict(
    {
        "1": {
            "id": "1",
            "name": "First",
        },
        "2": {
            "id": "2",
            "name": "Second",
        },
        "3": {
            "id": "3",
            "name": "Third",
        },
    }
)


@pytest.mark.unit
async def test_get_all() -> None:
    """Should return a non-empty collection."""
    guest_collection = await GuestService.get_all(repository=FakeRepository(_TEST_DB))
    assert type(guest_collection) == list
    assert len(guest_collection) == len(_TEST_DB.values())
    for s in guest_collection:
        assert type(s) == GuestModel
        assert s.id
        assert s.name


@pytest.mark.unit
async def test_get_by_id() -> None:
    """Should return a non-empty model."""
    hello_world = await GuestService.get(repository=FakeRepository(_TEST_DB), id="1")
    assert type(hello_world) == GuestModel
    assert identical_content(hello_world, _TEST_DB["1"])


def identical_content(s: Any, d: dict) -> bool:
    """Check for equal content."""
    return s.id == d["id"] and s.name == d["name"]
