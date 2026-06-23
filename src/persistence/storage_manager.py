import json
from typing import Any, Protocol


class StorageBackend(Protocol):
    """Protocol for key-value storage.

    In the browser this is implemented via localStorage.
    In tests this is replaced by a dict-based fake.
    """

    def get_item(self, key: str) -> str | None: ...

    def set_item(self, key: str, value: str) -> None: ...

    def remove_item(self, key: str) -> None: ...


class StorageManager:
    """Serializes/deserializes data to a StorageBackend as JSON."""

    def __init__(self, backend: StorageBackend) -> None:
        self._backend = backend

    def save(self, key: str, data: Any) -> None:
        serialized = json.dumps(data, ensure_ascii=False)
        self._backend.set_item(key, serialized)

    def load(self, key: str) -> Any | None:
        """Load and deserialize JSON from storage.

        Returns None if key does not exist.
        Raises ValueError if data exists but is not valid JSON.
        """
        raw = self._backend.get_item(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Corrupted data for key '{key}': {e}") from e

    def clear(self, key: str) -> None:
        self._backend.remove_item(key)
