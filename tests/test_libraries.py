import pytest

from src.domain.combo import Combo
from src.domain.custom_workout import CustomWorkout
from src.domain.footwork_move import FootworkMove
from src.domain.libraries import (
    ComboLibrary,
    CustomWorkoutLibrary,
    FootworkMoveLibrary,
)

# --- ComboLibrary ---


class TestComboLibrary:
    def test_add_and_list(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab, cross"))
        lib.add(Combo("Combo 2", "hook, uppercut"))
        assert len(lib) == 2
        assert [c.name for c in lib.list_all()] == ["Combo 1", "Combo 2"]

    def test_add_duplicate_name_raises(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        with pytest.raises(ValueError, match="already exists"):
            lib.add(Combo("Combo 1", "cross"))

    def test_get_by_name(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        assert lib.get_by_name("Combo 1").sequence == "jab"
        assert lib.get_by_name("nonexistent") is None

    def test_update(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        lib.update("Combo 1", Combo("Combo 1", "jab, cross"))
        assert lib.get_by_name("Combo 1").sequence == "jab, cross"

    def test_update_rename(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        lib.update("Combo 1", Combo("Combo A", "jab"))
        assert lib.get_by_name("Combo 1") is None
        assert lib.get_by_name("Combo A") is not None

    def test_update_rename_conflict_raises(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        lib.add(Combo("Combo 2", "cross"))
        with pytest.raises(ValueError, match="already exists"):
            lib.update("Combo 1", Combo("Combo 2", "jab"))

    def test_update_nonexistent_raises(self):
        lib = ComboLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.update("nope", Combo("nope", "jab"))

    def test_remove(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        lib.remove("Combo 1")
        assert len(lib) == 0

    def test_remove_nonexistent_raises(self):
        lib = ComboLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.remove("nope")

    def test_combos_property_returns_copy(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab"))
        combos = lib.combos
        combos.clear()
        assert len(lib) == 1

    def test_roundtrip_dict(self):
        lib = ComboLibrary()
        lib.add(Combo("Combo 1", "jab, cross"))
        lib.add(Combo("Combo 2", "hook"))
        restored = ComboLibrary.from_dict(lib.to_dict())
        assert len(restored) == 2
        assert restored.get_by_name("Combo 1").sequence == "jab, cross"


# --- FootworkMoveLibrary ---


class TestFootworkMoveLibrary:
    def test_add_and_list(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("lateral step"))
        lib.add(FootworkMove("retreat"))
        assert len(lib) == 2

    def test_add_duplicate_raises(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("lateral step"))
        with pytest.raises(ValueError, match="already exists"):
            lib.add(FootworkMove("lateral step"))

    def test_get_by_name(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("pivot"))
        assert lib.get_by_name("pivot") is not None
        assert lib.get_by_name("nope") is None

    def test_update(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("pivot"))
        lib.update("pivot", FootworkMove("pivot left"))
        assert lib.get_by_name("pivot") is None
        assert lib.get_by_name("pivot left") is not None

    def test_update_nonexistent_raises(self):
        lib = FootworkMoveLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.update("nope", FootworkMove("nope"))

    def test_remove(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("retreat"))
        lib.remove("retreat")
        assert len(lib) == 0

    def test_remove_nonexistent_raises(self):
        lib = FootworkMoveLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.remove("nope")

    def test_moves_property_returns_copy(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("retreat"))
        moves = lib.moves
        moves.clear()
        assert len(lib) == 1

    def test_roundtrip_dict(self):
        lib = FootworkMoveLibrary()
        lib.add(FootworkMove("lateral step"))
        lib.add(FootworkMove("retreat"))
        restored = FootworkMoveLibrary.from_dict(lib.to_dict())
        assert len(restored) == 2
        assert restored.get_by_name("lateral step") is not None


# --- CustomWorkoutLibrary ---


class TestCustomWorkoutLibrary:
    def test_add_and_list(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300))
        lib.add(CustomWorkout("Cardio", 600, "jump rope"))
        assert len(lib) == 2

    def test_add_duplicate_raises(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300))
        with pytest.raises(ValueError, match="already exists"):
            lib.add(CustomWorkout("Shadow", 600))

    def test_get_by_name(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300))
        assert lib.get_by_name("Shadow").duration == 300
        assert lib.get_by_name("nope") is None

    def test_update(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300))
        lib.update("Shadow", CustomWorkout("Shadow", 600, "longer session"))
        assert lib.get_by_name("Shadow").duration == 600

    def test_update_nonexistent_raises(self):
        lib = CustomWorkoutLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.update("nope", CustomWorkout("nope", 60))

    def test_remove(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300))
        lib.remove("Shadow")
        assert len(lib) == 0

    def test_remove_nonexistent_raises(self):
        lib = CustomWorkoutLibrary()
        with pytest.raises(KeyError, match="not found"):
            lib.remove("nope")

    def test_workouts_property_returns_copy(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300))
        workouts = lib.workouts
        workouts.clear()
        assert len(lib) == 1

    def test_roundtrip_dict(self):
        lib = CustomWorkoutLibrary()
        lib.add(CustomWorkout("Shadow", 300, "basic"))
        lib.add(CustomWorkout("Cardio", 600))
        restored = CustomWorkoutLibrary.from_dict(lib.to_dict())
        assert len(restored) == 2
        assert restored.get_by_name("Cardio").duration == 600
