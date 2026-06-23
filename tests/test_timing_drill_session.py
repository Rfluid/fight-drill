import random

import pytest

from src.domain.drill_config import TimingDrillConfig
from src.session.events import EventType
from src.session.timing_drill_session import TimingDrillSession


def _cfg(**overrides) -> TimingDrillConfig:
    defaults = dict(
        total_duration=10, min_interval=2, max_interval=4, target_technique="jab"
    )
    defaults.update(overrides)
    return TimingDrillConfig(**defaults)


def _collect(session) -> list:
    events = []
    session.on_event(events.append)
    return events


def _run_ticks(session, n: int) -> None:
    for _ in range(n):
        session.tick()


class TestTimingDrillSession:
    def test_session_ends_at_total_duration(self):
        rng = random.Random(42)
        s = TimingDrillSession(_cfg(total_duration=5), rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 10)

        assert s.is_finished is True
        types = [e.event_type for e in events]
        assert types[-1] == EventType.SESSION_END

    def test_stimuli_emitted_with_technique(self):
        rng = random.Random(42)
        s = TimingDrillSession(
            _cfg(total_duration=20, target_technique="teep"), rng=rng
        )
        events = _collect(s)
        s.start()
        _run_ticks(s, 20)

        stimuli = [e for e in events if e.event_type == EventType.STIMULUS]
        assert len(stimuli) >= 1
        for stim in stimuli:
            assert stim.data["technique"] == "teep"

    def test_stimuli_respect_interval_bounds(self):
        # With a deterministic seed we can verify all stimulus gaps
        rng = random.Random(123)
        cfg = _cfg(total_duration=50, min_interval=3, max_interval=7)
        s = TimingDrillSession(cfg, rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 50)

        stim_times = [s.elapsed]  # not useful, get from tracking
        # Re-run with tracking
        events2 = []
        elapsed_at_stim = []
        rng2 = random.Random(123)
        s2 = TimingDrillSession(cfg, rng=rng2)
        tick_count = 0

        def track(event):
            if event.event_type == EventType.STIMULUS:
                elapsed_at_stim.append(tick_count)

        s2.on_event(track)
        s2.start()
        for i in range(50):
            tick_count = i + 1
            s2.tick()

        # Check gaps between consecutive stimuli
        for i in range(1, len(elapsed_at_stim)):
            gap = elapsed_at_stim[i] - elapsed_at_stim[i - 1]
            assert 3 <= gap <= 7, f"Gap {gap} at index {i} out of bounds [3, 7]"

    def test_no_stimulus_after_session_end(self):
        rng = random.Random(42)
        s = TimingDrillSession(_cfg(total_duration=5), rng=rng)
        events = _collect(s)
        s.start()
        _run_ticks(s, 20)  # well past duration

        end_idx = next(
            i for i, e in enumerate(events) if e.event_type == EventType.SESSION_END
        )
        after_end = events[end_idx + 1 :] if end_idx + 1 < len(events) else []
        assert all(e.event_type != EventType.STIMULUS for e in after_end)

    def test_pause_prevents_progress(self):
        rng = random.Random(42)
        s = TimingDrillSession(_cfg(total_duration=20), rng=rng)
        s.start()
        s.tick()
        s.pause()
        elapsed_before = s.elapsed
        _run_ticks(s, 10)
        assert s.elapsed == elapsed_before

    def test_invalid_config_raises(self):
        with pytest.raises(ValueError):
            TimingDrillSession(_cfg(min_interval=5, max_interval=3))
