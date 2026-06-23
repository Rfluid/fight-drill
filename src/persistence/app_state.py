from typing import Any

from src.domain.libraries import (
    ComboLibrary,
    CustomWorkoutLibrary,
    FootworkMoveLibrary,
)

from .storage_manager import StorageManager

APP_STATE_KEY = "fightdrill_state"


class AppState:
    """Centralizes application state and persists via StorageManager (RNF07).

    On load, validates data structure. If corrupted or invalid,
    falls back to default empty state and reports the error.
    """

    def __init__(self, storage: StorageManager) -> None:
        self._storage = storage
        self.combo_library = ComboLibrary()
        self.footwork_library = FootworkMoveLibrary()
        self.workout_library = CustomWorkoutLibrary()
        self.audio_volume: float = 1.0
        self.voice_volume: float = 1.0
        self.voice_rate: float = 1.0
        self._load_error: str | None = None

    @property
    def load_error(self) -> str | None:
        return self._load_error

    def to_dict(self) -> dict:
        return {
            "combos": self.combo_library.to_dict(),
            "footwork_moves": self.footwork_library.to_dict(),
            "custom_workouts": self.workout_library.to_dict(),
            "audio_volume": self.audio_volume,
            "voice_volume": self.voice_volume,
            "voice_rate": self.voice_rate,
        }

    def _load_from_dict(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise ValueError("State data must be a dictionary.")

        required_keys = {"combos", "footwork_moves", "custom_workouts"}
        missing = required_keys - set(data.keys())
        if missing:
            raise ValueError(f"Missing keys in state data: {missing}")

        self.combo_library = ComboLibrary.from_dict(data["combos"])
        self.footwork_library = FootworkMoveLibrary.from_dict(data["footwork_moves"])
        self.workout_library = CustomWorkoutLibrary.from_dict(data["custom_workouts"])
        self.audio_volume = float(data.get("audio_volume", 1.0))
        self.voice_volume = float(data.get("voice_volume", 1.0))
        self.voice_rate = float(data.get("voice_rate", 1.0))

    def save(self) -> None:
        self._storage.save(APP_STATE_KEY, self.to_dict())

    def load(self) -> bool:
        """Load state from storage. Returns True if loaded successfully.

        If data is missing, keeps default empty state (not an error).
        If data is corrupted/invalid, resets to default and sets load_error.
        """
        self._load_error = None

        try:
            raw = self._storage.load(APP_STATE_KEY)
        except ValueError as e:
            self._reset_to_default()
            self._load_error = str(e)
            return False

        if raw is None:
            return True

        try:
            self._load_from_dict(raw)
            return True
        except (ValueError, KeyError, TypeError) as e:
            self._reset_to_default()
            self._load_error = str(e)
            return False

    def _reset_to_default(self) -> None:
        self.combo_library = ComboLibrary()
        self.footwork_library = FootworkMoveLibrary()
        self.workout_library = CustomWorkoutLibrary()
