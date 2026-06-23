import random

import pytest

from src.domain.call_mode import CallMode
from src.domain.combo import Combo
from src.domain.drill_config import ComboDrillConfig
from src.session.combo_drill_session import ComboDrillSession
from src.session.events import EventType


def _combos(n: int = 3) -> list[Combo]:
    return [Combo(f"Combo {i + 1}", f"technique {i + 1}") for i in range(n)]


def _cfg(**overrides) -> ComboDrillConfig:
    defaults = dict(
        combos=_combos(3),
        call_mode=CallMode.SEQUENTIAL,
        call_interval=2,
        total_duration=10,
    )
    defaults.update(overrides)
    return ComboDrillConfig(**defaults)


def _collect(session) -> list:
    events = []
    session.on_event(events.append)
    return events


def _run_ticks(session, n: int) -> None:
    for _ in range(n):
        session.tick()


class TestComboDrillSequential:
    def test_first_combo_called_on_start(self):
        s = ComboDrillSession(_cfg())
        events = _collect(s)
        s.start()
        assert events[0].event_type == EventType.COMBO_CALL
        assert events[0].data["combo_name"] == "Combo 1"

    def test_sequential_cycles_through_combos(self):
        s = ComboDrillSession(_cfg(call_interval=1, total_duration=10))
        events = _collect(s)
        s.start()  # calls Combo 1
        _run_ticks(s, 6)

        combo_calls = [e for e in events if e.event_type == EventType.COMBO_CALL]
        names = [c.data["combo_name"] for c in combo_calls]
        # start=Combo1, tick1=Combo2, tick2=Combo3, tick3=Combo1, tick4=Combo2, tick5=Combo3, tick6=Combo1
        assert names == [
            "Combo 1",
            "Combo 2",
            "Combo 3",
            "Combo 1",
            "Combo 2",
            "Combo 3",
            "Combo 1",
        ]

    def test_session_ends_at_total_duration(self):
        s = ComboDrillSession(_cfg(total_duration=5))
        events = _collect(s)
        s.start()
        _run_ticks(s, 10)

        assert s.is_finished is True
        types = [e.event_type for e in events]
        assert types[-1] == EventType.SESSION_END


class TestComboDrillRandom:
    def test_no_consecutive_repeats(self):
        rng = random.Random(42)
        cfg = _cfg(
            combos=_combos(4),
            call_mode=CallMode.RANDOM,
            call_interval=1,
            total_duration=50,
        )
        s = ComboDrillSession(cfg, rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 50)

        combo_calls = [e for e in events if e.event_type == EventType.COMBO_CALL]
        names = [c.data["combo_name"] for c in combo_calls]

        for i in range(1, len(names)):
            assert names[i] != names[i - 1], (
                f"Consecutive repeat at index {i}: {names[i]}"
            )

    def test_single_combo_random_always_returns_it(self):
        rng = random.Random(42)
        cfg = _cfg(
            combos=[Combo("Only", "jab")],
            call_mode=CallMode.RANDOM,
            call_interval=1,
            total_duration=5,
        )
        s = ComboDrillSession(cfg, rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 5)

        combo_calls = [e for e in events if e.event_type == EventType.COMBO_CALL]
        assert all(c.data["combo_name"] == "Only" for c in combo_calls)

    def test_random_uses_all_combos_eventually(self):
        rng = random.Random(42)
        combos = _combos(3)
        cfg = _cfg(
            combos=combos,
            call_mode=CallMode.RANDOM,
            call_interval=1,
            total_duration=100,
        )
        s = ComboDrillSession(cfg, rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 100)

        called_names = {
            e.data["combo_name"] for e in events if e.event_type == EventType.COMBO_CALL
        }
        expected_names = {c.name for c in combos}
        assert called_names == expected_names


class TestComboDrillComboData:
    def test_combo_call_includes_sequence(self):
        s = ComboDrillSession(_cfg())
        events = _collect(s)
        s.start()
        call = events[0]
        assert call.data["combo_sequence"] == "technique 1"


class TestComboDrillValidation:
    def test_empty_combos_raises(self):
        with pytest.raises(ValueError, match="At least one combo"):
            ComboDrillSession(
                ComboDrillConfig(combos=[], call_interval=1, total_duration=10)
            )
