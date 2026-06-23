import random

import pytest

from src.domain.drill_config import FootworkDrillConfig
from src.domain.footwork_move import FootworkMove
from src.session.events import EventType
from src.session.footwork_drill_session import FootworkDrillSession


def _moves(n: int = 3) -> list[FootworkMove]:
    names = ["lateral step", "retreat", "pivot left", "advance", "switch stance"]
    return [FootworkMove(names[i]) for i in range(n)]


def _cfg(**overrides) -> FootworkDrillConfig:
    defaults = dict(
        moves=_moves(3),
        min_interval=2,
        max_interval=4,
        total_duration=15,
    )
    defaults.update(overrides)
    return FootworkDrillConfig(**defaults)


def _collect(session) -> list:
    events = []
    session.on_event(events.append)
    return events


def _run_ticks(session, n: int) -> None:
    for _ in range(n):
        session.tick()


class TestFootworkDrillSession:
    def test_first_move_called_on_start(self):
        rng = random.Random(42)
        s = FootworkDrillSession(_cfg(), rng=rng)
        events = _collect(s)
        s.start()
        assert events[0].event_type == EventType.MOVE_CALL
        assert events[0].data["move_name"] in {"lateral step", "retreat", "pivot left"}

    def test_session_ends_at_total_duration(self):
        rng = random.Random(42)
        s = FootworkDrillSession(_cfg(total_duration=5), rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 10)

        assert s.is_finished is True
        types = [e.event_type for e in events]
        assert types[-1] == EventType.SESSION_END

    def test_moves_called_at_random_intervals(self):
        rng = random.Random(123)
        cfg = _cfg(total_duration=50, min_interval=3, max_interval=6)
        elapsed_at_call = []
        tick_count = 0

        s = FootworkDrillSession(cfg, rng=rng)

        def track(event):
            if event.event_type == EventType.MOVE_CALL:
                elapsed_at_call.append(tick_count)

        s.on_event(track)
        s.start()  # first call at tick_count=0
        for i in range(50):
            tick_count = i + 1
            s.tick()

        # Check gaps between calls (skip first since it's at start)
        for i in range(2, len(elapsed_at_call)):
            gap = elapsed_at_call[i] - elapsed_at_call[i - 1]
            assert 3 <= gap <= 6, f"Gap {gap} at index {i} out of bounds [3, 6]"

    def test_all_moves_used_eventually(self):
        rng = random.Random(42)
        moves = _moves(3)
        cfg = _cfg(moves=moves, total_duration=100, min_interval=1, max_interval=2)
        s = FootworkDrillSession(cfg, rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 100)

        called_names = {
            e.data["move_name"] for e in events if e.event_type == EventType.MOVE_CALL
        }
        expected = {m.name for m in moves}
        assert called_names == expected

    def test_single_move_always_called(self):
        rng = random.Random(42)
        cfg = _cfg(
            moves=[FootworkMove("only move")],
            min_interval=1,
            max_interval=2,
            total_duration=5,
        )
        s = FootworkDrillSession(cfg, rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 5)

        move_calls = [e for e in events if e.event_type == EventType.MOVE_CALL]
        assert all(c.data["move_name"] == "only move" for c in move_calls)

    def test_no_moves_after_session_end(self):
        rng = random.Random(42)
        s = FootworkDrillSession(_cfg(total_duration=5), rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 20)

        end_idx = next(
            i for i, e in enumerate(events) if e.event_type == EventType.SESSION_END
        )
        after_end = events[end_idx + 1 :] if end_idx + 1 < len(events) else []
        assert all(e.event_type != EventType.MOVE_CALL for e in after_end)


class TestFootworkDrillValidation:
    def test_no_moves_raises(self):
        with pytest.raises(ValueError, match="At least one footwork move"):
            FootworkDrillSession(
                FootworkDrillConfig(
                    moves=[], min_interval=2, max_interval=4, total_duration=10
                )
            )

    def test_min_ge_max_raises(self):
        with pytest.raises(ValueError, match="strictly less"):
            FootworkDrillSession(_cfg(min_interval=5, max_interval=5))
