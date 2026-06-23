import pytest

from src.domain.custom_workout import CustomWorkout


class TestCustomWorkout:
    def test_create_valid_workout(self):
        w = CustomWorkout(name="Shadow Boxing", duration=300, description="3x rounds")
        assert w.name == "Shadow Boxing"
        assert w.duration == 300
        assert w.description == "3x rounds"

    def test_description_defaults_to_empty(self):
        w = CustomWorkout(name="Cardio", duration=600)
        assert w.description == ""

    def test_name_stripped(self):
        w = CustomWorkout(name="  Cardio  ", duration=60)
        assert w.name == "Cardio"

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            CustomWorkout(name="", duration=60)

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            CustomWorkout(name="   ", duration=60)

    def test_zero_duration_raises(self):
        with pytest.raises(ValueError, match="duration must be greater than zero"):
            CustomWorkout(name="Cardio", duration=0)

    def test_negative_duration_raises(self):
        with pytest.raises(ValueError, match="duration must be greater than zero"):
            CustomWorkout(name="Cardio", duration=-10)

    def test_to_dict(self):
        w = CustomWorkout(name="Cardio", duration=60, description="light")
        assert w.to_dict() == {
            "name": "Cardio",
            "duration": 60,
            "description": "light",
        }

    def test_from_dict(self):
        data = {"name": "Cardio", "duration": 60, "description": "light"}
        w = CustomWorkout.from_dict(data)
        assert w.name == "Cardio"
        assert w.duration == 60
        assert w.description == "light"

    def test_from_dict_missing_description(self):
        data = {"name": "Cardio", "duration": 60}
        w = CustomWorkout.from_dict(data)
        assert w.description == ""

    def test_roundtrip_dict(self):
        original = CustomWorkout(name="Shadow Boxing", duration=300, description="3x")
        restored = CustomWorkout.from_dict(original.to_dict())
        assert restored == original
