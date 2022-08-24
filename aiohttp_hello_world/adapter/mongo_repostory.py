"""Module for fetching entity descriptions."""
from typing import Any, List, Optional

from aiohttp_hello_world.adapter.abstract_repostory import AbstractRepository
from aiohttp_hello_world.model import GuestModel


class MongoRepository(AbstractRepository):
    """Class representing a mongo repository."""

    _db: Any

    def __init__(self, db: Any) -> None:  # pragma: no cover
        """Initialize the fake repository."""
        self._db = db

    async def get_all(self) -> Optional[List[GuestModel]]:  # pragma: no cover
        """Get all entities in store."""
        guests: List[GuestModel] = []
        cursor = self._db.guests_collection.find()
        for guest in await cursor.to_list(None):
            guests.append(GuestModel.from_dict(guest))
        return guests

    async def get(self, id: str) -> Optional[GuestModel]:  # pragma: no cover
        """Get entity given by id if in objects in store."""
        result = await self._db.guests_collection.find_one({"id": id})
        if result:
            return GuestModel.from_dict(result)
        return None

    async def add(self: Any, data: GuestModel) -> Optional[str]:  # pragma: no cover
        """Create id and add new entity to store."""
        new_id = await self._db.guests_collection.count_documents({}) + 1
        new_guest = data.to_dict()
        new_guest["id"] = str(new_id)
        result = await self._db.guests_collection.insert_one(new_guest)
        if result.acknowledged:
            return str(new_id)
        return None

    async def delete(self, id: str) -> bool:  # pragma: no cover
        """Delete entity given by id if in objects in store."""
        result = await self._db.guests_collection.delete_one({"id": id})
        if result:
            return True
        return False
