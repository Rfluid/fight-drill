

class FakeStorageBackend:
    """In-memory StorageBackend for testing."""

    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    def get_item(self, key: str) -> str | None:
        return self._data.get(key)

    def set_item(self, key: str, value: str) -> None:
        self._data[key] = value

    def remove_item(self, key: str) -> None:
        self._data.pop(key, None)
