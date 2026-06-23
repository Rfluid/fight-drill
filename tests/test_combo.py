import pytest

from src.domain.combo import Combo


class TestCombo:
    def test_create_valid_combo(self):
        combo = Combo(name="Combo 1", sequence="jab, cross, hook")
        assert combo.name == "Combo 1"
        assert combo.sequence == "jab, cross, hook"

    def test_name_is_stripped(self):
        combo = Combo(name="  Combo 1  ", sequence="jab")
        assert combo.name == "Combo 1"

    def test_sequence_is_stripped(self):
        combo = Combo(name="Combo 1", sequence="  jab, cross  ")
        assert combo.sequence == "jab, cross"

    def test_empty_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            Combo(name="", sequence="jab")

    def test_whitespace_only_name_raises(self):
        with pytest.raises(ValueError, match="name must not be empty"):
            Combo(name="   ", sequence="jab")

    def test_to_dict(self):
        combo = Combo(name="Combo 1", sequence="jab, cross")
        assert combo.to_dict() == {"name": "Combo 1", "sequence": "jab, cross"}

    def test_from_dict(self):
        data = {"name": "Combo 1", "sequence": "jab, cross"}
        combo = Combo.from_dict(data)
        assert combo.name == "Combo 1"
        assert combo.sequence == "jab, cross"

    def test_roundtrip_dict(self):
        original = Combo(name="Combo 1", sequence="jab, cross, hook")
        restored = Combo.from_dict(original.to_dict())
        assert restored == original

    def test_equality(self):
        a = Combo(name="Combo 1", sequence="jab")
        b = Combo(name="Combo 1", sequence="jab")
        assert a == b

    def test_inequality(self):
        a = Combo(name="Combo 1", sequence="jab")
        b = Combo(name="Combo 2", sequence="jab")
        assert a != b
