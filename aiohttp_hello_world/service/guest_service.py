"""Module for hello_world service."""
from typing import Any, List


from aiohttp_hello_world.model.guest_modell import GuestModel


class GetError(Exception):
    """Class representing a get error."""

    pass


class CreateError(Exception):
    """Class representing a get error."""

    pass


class GuestService:
    """Class representing hello_world service."""

    @classmethod
    async def get_all(cls: Any, repository: Any) -> List[GuestModel]:
        """Get function."""
        list = await repository.get_all()
        return list if list else []

    @classmethod
    async def create(cls: Any, repository: Any, data: GuestModel) -> str:
        """Get function."""
        id = await repository.add(data=data)
        if id is None:
            raise CreateError("Could not create hello_world.")
        return id

    @classmethod
    async def get(cls: Any, repository: Any, id: str) -> GuestModel:
        """Get function."""
        name = await repository.get(id=id)
        if name is None:
            raise GetError(f"Hello world with id {id} not found.")
        return name

    @classmethod
    async def delete(cls: Any, repository: Any, id: str) -> bool:
        """Get function."""
        id = await repository.delete(id=id)
        if not id:
            raise GetError(f"Hello world with id {id} not found.")
        return True
