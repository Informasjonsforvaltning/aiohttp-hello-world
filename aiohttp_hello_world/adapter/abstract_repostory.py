"""Module for fetching entity descriptions."""
import abc
from typing import Any, List, Optional

from aiohttp_hello_world.model import GuestModel


class AbstractRepository(abc.ABC):
    """Class representing an abstract repository."""

    @abc.abstractmethod
    async def get_all(self) -> Optional[List[GuestModel]]:  # pragma: no cover
        """Get all entities in store."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def get(self, id: str) -> Optional[GuestModel]:  # pragma: no cover
        """Get entity given by id if in objects in store."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(self: Any, data: GuestModel) -> Optional[str]:  # pragma: no cover
        """Create id and add new entity to store."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, id: str) -> bool:  # pragma: no cover
        """Get entity given by id if in objects in store."""
        raise NotImplementedError()
