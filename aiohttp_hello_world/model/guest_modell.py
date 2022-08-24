"""GraphDescription details data class."""
from dataclasses import dataclass, field
from typing import Optional

from dataclasses_json import DataClassJsonMixin


@dataclass
class GuestModel(DataClassJsonMixin):
    """Abstract data class with details regarding a graph."""

    name: str
    id: Optional[str] = field(default=None)
