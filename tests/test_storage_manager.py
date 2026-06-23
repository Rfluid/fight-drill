import pytest

from src.persistence.storage_manager import StorageManager
from tests.fake_storage import FakeStorageBackend


class TestStorageManager:
    def _make(self) -> tuple[StorageManager, FakeStorageBackend]:
        backend = FakeStorageBackend()
        return StorageManager(backend), backend

    def test_save_and_load_dict(self):
        sm, _ = self._make()
        sm.save("key", {"a": 1, "b": [2, 3]})
        assert sm.load("key") == {"a": 1, "b": [2, 3]}

    def test_save_and_load_list(self):
        sm, _ = self._make()
        sm.save("key", [1, 2, 3])
        assert sm.load("key") == [1, 2, 3]

    def test_save_and_load_string(self):
        sm, _ = self._make()
        sm.save("key", "hello")
        assert sm.load("key") == "hello"

    def test_save_and_load_unicode(self):
        sm, _ = self._make()
        sm.save("key", {"nome": "passo lateral direito"})
        assert sm.load("key") == {"nome": "passo lateral direito"}

    def test_load_missing_key_returns_none(self):
        sm, _ = self._make()
        assert sm.load("nonexistent") is None

    def test_load_corrupted_json_raises_value_error(self):
        sm, backend = self._make()
        backend.set_item("key", "not valid json{{{")
        with pytest.raises(ValueError, match="Corrupted data"):
            sm.load("key")

    def test_clear(self):
        sm, _ = self._make()
        sm.save("key", {"a": 1})
        sm.clear("key")
        assert sm.load("key") is None

    def test_clear_nonexistent_key_does_not_raise(self):
        sm, _ = self._make()
        sm.clear("nonexistent")  # should not raise

    def test_overwrite(self):
        sm, _ = self._make()
        sm.save("key", {"v": 1})
        sm.save("key", {"v": 2})
        assert sm.load("key") == {"v": 2}

    def test_multiple_keys(self):
        sm, _ = self._make()
        sm.save("a", 1)
        sm.save("b", 2)
        assert sm.load("a") == 1
        assert sm.load("b") == 2
