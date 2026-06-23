import pytest

from src.domain.footwork_move import FootworkMove


class TestFootworkMove:
    def test_create_valid_move(self):
        move = FootworkMove(name="lateral step right")
        assert move.name == "lateral step right"

    def test_name_is_stripped(self):
        move = FootworkMove(name="  pivot left  ")
        assert move.name == "pivot left"

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            FootworkMove(name="")

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            FootworkMove(name="   ")

    def test_to_dict(self):
        move = FootworkMove(name="retreat")
        assert move.to_dict() == {"name": "retreat"}

    def test_from_dict(self):
        move = FootworkMove.from_dict({"name": "retreat"})
        assert move.name == "retreat"

    def test_roundtrip_dict(self):
        original = FootworkMove(name="pivot left")
        restored = FootworkMove.from_dict(original.to_dict())
        assert restored == original
