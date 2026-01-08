import json
from typing import Any


class OsduDataUnit:
    """Wrapper for OSDU test data (records, manifests, workflows)."""

    def __init__(self, data_id: str, data_unit: dict[str, Any]):
        self._id = data_id
        self._data_unit = data_unit

    def get_id(self) -> str:
        """Get the data unit ID."""
        return self._id

    def get_data_unit(self) -> dict[str, Any]:
        """Get the data unit object."""
        return self._data_unit

    def stringify(self) -> str:
        """Convert data unit to JSON string."""
        return json.dumps(self._data_unit, indent=2)
