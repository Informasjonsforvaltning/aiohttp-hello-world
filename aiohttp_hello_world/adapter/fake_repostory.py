"""Module for fetching entity descriptions."""
from typing import Any, Dict, List, Optional

from aiohttp_hello_world.adapter.abstract_repostory import AbstractRepository
from aiohttp_hello_world.model import GuestModel


class FakeRepository(AbstractRepository):
    """Class representing an hello world adapter.

    Implements basic fetch methods:
    - get_all
    - get_by_id
    """

    _db: Dict[str, Dict] = dict()

    def __init__(self, db: Dict[str, Dict]) -> None:
        """Initialize the fake repository."""
        self._db = db

    async def get_all(self) -> Optional[List[GuestModel]]:  # pragma: no cover
        """Get all entities in store."""
        _values = [value for value in self._db.values()]
        values: List[GuestModel] = []
        for value in _values:
            values.append(GuestModel.from_dict(value))
        return values

    async def get(self, id: str) -> Optional[GuestModel]:  # pragma: no cover
        """Get entity given by id if in objects in store."""
        if id in self._db:
            return GuestModel(**self._db[id])
        return None

    async def add(self: Any, data: GuestModel) -> Optional[str]:  # pragma: no cover
        """Create id and add new entity to store."""
        new_id = str(len(self._db) + 1)
        self._db[new_id] = data.to_dict()
        self._db[new_id]["id"] = new_id
        return new_id

    async def delete(self: Any, id: str) -> bool:  # pragma: no cover
        """Delete entity given by id if in objects in store."""
        if id in self._db:
            del self._db[id]
            return True
        return False
