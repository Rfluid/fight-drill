import pytest

from src.domain.call_mode import CallMode
from src.domain.combo import Combo
from src.domain.drill_config import (
    ComboDrillConfig,
    FootworkDrillConfig,
    RoundTimerConfig,
    TimingDrillConfig,
)
from src.domain.footwork_move import FootworkMove

# --- RoundTimerConfig ---


class TestRoundTimerConfig:
    def _valid(self, **overrides) -> RoundTimerConfig:
        defaults = dict(
            num_rounds=3, work_duration=180, rest_duration=60, warning_time=10
        )
        defaults.update(overrides)
        return RoundTimerConfig(**defaults)

    def test_valid_config(self):
        cfg = self._valid()
        cfg.validate()  # should not raise

    def test_zero_rounds_raises(self):
        cfg = self._valid(num_rounds=0)
        with pytest.raises(ValueError, match="rounds"):
            cfg.validate()

    def test_zero_work_duration_raises(self):
        cfg = self._valid(work_duration=0)
        with pytest.raises(ValueError, match="Work duration"):
            cfg.validate()

    def test_negative_rest_raises(self):
        cfg = self._valid(rest_duration=-1)
        with pytest.raises(ValueError, match="Rest duration"):
            cfg.validate()

    def test_negative_warning_raises(self):
        cfg = self._valid(warning_time=-1)
        with pytest.raises(ValueError, match="Warning time must not be negative"):
            cfg.validate()

    def test_warning_ge_work_raises(self):
        cfg = self._valid(work_duration=60, warning_time=60)
        with pytest.raises(ValueError, match="Warning time must be less"):
            cfg.validate()

    def test_to_dict(self):
        cfg = self._valid()
        d = cfg.to_dict()
        assert d["type"] == "round_timer"
        assert d["num_rounds"] == 3

    def test_roundtrip_dict(self):
        original = self._valid()
        restored = RoundTimerConfig.from_dict(original.to_dict())
        assert restored == original


# --- TimingDrillConfig ---


class TestTimingDrillConfig:
    def _valid(self, **overrides) -> TimingDrillConfig:
        defaults = dict(
            total_duration=180, min_interval=2, max_interval=8, target_technique="jab"
        )
        defaults.update(overrides)
        return TimingDrillConfig(**defaults)

    def test_valid_config(self):
        cfg = self._valid()
        cfg.validate()

    def test_zero_duration_raises(self):
        cfg = self._valid(total_duration=0)
        with pytest.raises(ValueError, match="Total duration"):
            cfg.validate()

    def test_min_interval_zero_raises(self):
        cfg = self._valid(min_interval=0)
        with pytest.raises(ValueError, match="Minimum interval must be greater"):
            cfg.validate()

    def test_min_ge_max_raises(self):
        cfg = self._valid(min_interval=5, max_interval=5)
        with pytest.raises(ValueError, match="strictly less"):
            cfg.validate()

    def test_min_greater_than_max_raises(self):
        cfg = self._valid(min_interval=10, max_interval=5)
        with pytest.raises(ValueError, match="strictly less"):
            cfg.validate()

    def test_empty_technique_raises(self):
        cfg = self._valid(target_technique="   ")
        with pytest.raises(ValueError, match="Target technique"):
            cfg.validate()

    def test_roundtrip_dict(self):
        original = self._valid()
        restored = TimingDrillConfig.from_dict(original.to_dict())
        assert restored == original


# --- ComboDrillConfig ---


class TestComboDrillConfig:
    def _valid(self, **overrides) -> ComboDrillConfig:
        defaults = dict(
            combos=[Combo("Combo 1", "jab, cross")],
            call_mode=CallMode.SEQUENTIAL,
            call_interval=5,
            total_duration=180,
        )
        defaults.update(overrides)
        return ComboDrillConfig(**defaults)

    def test_valid_config(self):
        cfg = self._valid()
        cfg.validate()

    def test_no_combos_raises(self):
        cfg = self._valid(combos=[])
        with pytest.raises(ValueError, match="At least one combo"):
            cfg.validate()

    def test_zero_interval_raises(self):
        cfg = self._valid(call_interval=0)
        with pytest.raises(ValueError, match="Call interval"):
            cfg.validate()

    def test_zero_duration_raises(self):
        cfg = self._valid(total_duration=0)
        with pytest.raises(ValueError, match="Total duration"):
            cfg.validate()

    def test_roundtrip_dict(self):
        original = self._valid()
        restored = ComboDrillConfig.from_dict(original.to_dict())
        assert restored == original

    def test_call_mode_preserved_in_dict(self):
        cfg = self._valid(call_mode=CallMode.RANDOM)
        d = cfg.to_dict()
        assert d["call_mode"] == "random"
        restored = ComboDrillConfig.from_dict(d)
        assert restored.call_mode == CallMode.RANDOM


# --- FootworkDrillConfig ---


class TestFootworkDrillConfig:
    def _valid(self, **overrides) -> FootworkDrillConfig:
        defaults = dict(
            moves=[FootworkMove("lateral step")],
            min_interval=2,
            max_interval=5,
            total_duration=180,
        )
        defaults.update(overrides)
        return FootworkDrillConfig(**defaults)

    def test_valid_config(self):
        cfg = self._valid()
        cfg.validate()

    def test_no_moves_raises(self):
        cfg = self._valid(moves=[])
        with pytest.raises(ValueError, match="At least one footwork move"):
            cfg.validate()

    def test_min_ge_max_raises(self):
        cfg = self._valid(min_interval=5, max_interval=5)
        with pytest.raises(ValueError, match="strictly less"):
            cfg.validate()

    def test_zero_min_interval_raises(self):
        cfg = self._valid(min_interval=0)
        with pytest.raises(ValueError, match="Minimum interval must be greater"):
            cfg.validate()

    def test_zero_duration_raises(self):
        cfg = self._valid(total_duration=0)
        with pytest.raises(ValueError, match="Total duration"):
            cfg.validate()

    def test_roundtrip_dict(self):
        original = self._valid()
        restored = FootworkDrillConfig.from_dict(original.to_dict())
        assert restored == original
