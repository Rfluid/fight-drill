"""Browser-specific storage backend using PyScript/Pyodide js interop.

Only importable inside a PyScript environment.
Implements the StorageBackend protocol.
"""



class LocalStorageBackend:
    """StorageBackend implementation using browser localStorage."""

    def get_item(self, key: str) -> str | None:
        from js import window  # type: ignore[import-not-found]

        value = window.localStorage.getItem(key)
        if value is None:
            return None
        return str(value)

    def set_item(self, key: str, value: str) -> None:
        from js import window  # type: ignore[import-not-found]

        window.localStorage.setItem(key, value)

    def remove_item(self, key: str) -> None:
        from js import window  # type: ignore[import-not-found]

        window.localStorage.removeItem(key)
