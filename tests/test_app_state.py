import json

from src.domain.combo import Combo
from src.domain.custom_workout import CustomWorkout
from src.domain.footwork_move import FootworkMove
from src.persistence.app_state import APP_STATE_KEY, AppState
from src.persistence.storage_manager import StorageManager
from tests.fake_storage import FakeStorageBackend


def _make() -> tuple[AppState, FakeStorageBackend]:
    backend = FakeStorageBackend()
    storage = StorageManager(backend)
    return AppState(storage), backend


def _populated_state(state: AppState) -> None:
    state.combo_library.add(Combo("Combo 1", "jab, cross"))
    state.combo_library.add(Combo("Combo 2", "hook, uppercut"))
    state.footwork_library.add(FootworkMove("lateral step"))
    state.footwork_library.add(FootworkMove("retreat"))
    state.workout_library.add(CustomWorkout("Shadow Boxing", 300, "3 rounds"))


class TestAppStateToDict:
    def test_empty_state(self):
        state, _ = _make()
        d = state.to_dict()
        assert d == {
            "combos": [],
            "footwork_moves": [],
            "custom_workouts": [],
            "audio_volume": 1.0,
            "voice_volume": 1.0,
            "voice_rate": 1.0,
        }

    def test_populated_state(self):
        state, _ = _make()
        _populated_state(state)
        d = state.to_dict()
        assert len(d["combos"]) == 2
        assert len(d["footwork_moves"]) == 2
        assert len(d["custom_workouts"]) == 1
        assert d["combos"][0]["name"] == "Combo 1"


class TestAppStateSaveLoad:
    def test_save_and_load_roundtrip(self):
        state, backend = _make()
        _populated_state(state)
        state.save()

        state2 = AppState(StorageManager(backend))
        result = state2.load()

        assert result is True
        assert state2.load_error is None
        assert len(state2.combo_library) == 2
        assert len(state2.footwork_library) == 2
        assert len(state2.workout_library) == 1
        assert state2.combo_library.get_by_name("Combo 1").sequence == "jab, cross"
        assert state2.footwork_library.get_by_name("retreat") is not None
        assert state2.workout_library.get_by_name("Shadow Boxing").duration == 300

    def test_load_empty_storage_keeps_defaults(self):
        state, _ = _make()
        result = state.load()
        assert result is True
        assert state.load_error is None
        assert len(state.combo_library) == 0
        assert len(state.footwork_library) == 0
        assert len(state.workout_library) == 0

    def test_save_overwrites_previous(self):
        state, backend = _make()
        state.combo_library.add(Combo("Old", "jab"))
        state.save()

        state.combo_library.remove("Old")
        state.combo_library.add(Combo("New", "cross"))
        state.save()

        state2 = AppState(StorageManager(backend))
        state2.load()
        assert state2.combo_library.get_by_name("Old") is None
        assert state2.combo_library.get_by_name("New") is not None


class TestAppStateCorruptedData:
    def test_corrupted_json_resets_to_default(self):
        state, backend = _make()
        backend.set_item(APP_STATE_KEY, "not json{{{")
        result = state.load()
        assert result is False
        assert state.load_error is not None
        assert len(state.combo_library) == 0

    def test_wrong_type_resets_to_default(self):
        state, backend = _make()
        backend.set_item(APP_STATE_KEY, json.dumps([1, 2, 3]))
        result = state.load()
        assert result is False
        assert "dictionary" in state.load_error

    def test_missing_keys_resets_to_default(self):
        state, backend = _make()
        backend.set_item(APP_STATE_KEY, json.dumps({"combos": []}))
        result = state.load()
        assert result is False
        assert "Missing keys" in state.load_error

    def test_invalid_combo_data_resets_to_default(self):
        state, backend = _make()
        bad_data = {
            "combos": [{"bad_field": "value"}],
            "footwork_moves": [],
            "custom_workouts": [],
        }
        backend.set_item(APP_STATE_KEY, json.dumps(bad_data))
        result = state.load()
        assert result is False
        assert state.load_error is not None
        assert len(state.combo_library) == 0

    def test_invalid_workout_duration_resets_to_default(self):
        state, backend = _make()
        bad_data = {
            "combos": [],
            "footwork_moves": [],
            "custom_workouts": [{"name": "Bad", "duration": -1}],
        }
        backend.set_item(APP_STATE_KEY, json.dumps(bad_data))
        result = state.load()
        assert result is False
        assert state.load_error is not None

    def test_load_error_cleared_on_successful_load(self):
        state, backend = _make()
        # First: corrupt load
        backend.set_item(APP_STATE_KEY, "garbage")
        state.load()
        assert state.load_error is not None

        # Second: fix data and reload
        backend.remove_item(APP_STATE_KEY)
        result = state.load()
        assert result is True
        assert state.load_error is None
