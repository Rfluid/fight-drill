import pytest

from src.domain.drill_config import RoundTimerConfig
from src.session.events import DrillEvent, EventType
from src.session.round_timer_session import RoundTimerSession


def _cfg(**overrides) -> RoundTimerConfig:
    defaults = dict(num_rounds=2, work_duration=3, rest_duration=2, warning_time=1)
    defaults.update(overrides)
    return RoundTimerConfig(**defaults)


def _collect(session) -> list[DrillEvent]:
    events: list[DrillEvent] = []
    session.on_event(events.append)
    return events


def _run_ticks(session, n: int) -> None:
    for _ in range(n):
        session.tick()


class TestRoundTimerSessionBasic:
    def test_initial_state(self):
        s = RoundTimerSession(_cfg())
        assert s.is_running is False
        assert s.is_paused is False
        assert s.is_finished is False
        assert s.elapsed == 0

    def test_start_emits_round_start(self):
        s = RoundTimerSession(_cfg())
        events = _collect(s)
        s.start()
        assert len(events) == 1
        assert events[0].event_type == EventType.ROUND_START
        assert events[0].data["round"] == 1

    def test_pause_and_resume(self):
        s = RoundTimerSession(_cfg())
        s.start()
        s.pause()
        assert s.is_paused is True
        elapsed_before = s.elapsed
        _run_ticks(s, 5)
        assert s.elapsed == elapsed_before  # no progress while paused
        s.resume()
        assert s.is_paused is False
        s.tick()
        assert s.elapsed == elapsed_before + 1

    def test_stop(self):
        s = RoundTimerSession(_cfg())
        s.start()
        s.stop()
        assert s.is_finished is True
        assert s.is_running is False

    def test_start_after_finished_does_nothing(self):
        s = RoundTimerSession(_cfg())
        s.start()
        s.stop()
        events = _collect(s)
        s.start()
        assert events == []
        assert s.is_running is False


class TestRoundTimerSessionWorkPhase:
    def test_warning_fires_at_correct_time(self):
        # work=3, warning=1 → warning at elapsed second 2 (1s remaining)
        s = RoundTimerSession(_cfg(work_duration=3, warning_time=1))
        events = _collect(s)
        s.start()
        events.clear()

        s.tick()  # elapsed=1, remaining=2
        assert not any(e.event_type == EventType.ROUND_WARNING for e in events)

        s.tick()  # elapsed=2, remaining=1 → warning
        assert any(e.event_type == EventType.ROUND_WARNING for e in events)

    def test_warning_fires_only_once(self):
        s = RoundTimerSession(_cfg(work_duration=4, warning_time=2))
        events = _collect(s)
        s.start()
        events.clear()

        _run_ticks(s, 4)
        warnings = [e for e in events if e.event_type == EventType.ROUND_WARNING]
        assert len(warnings) == 1

    def test_no_warning_when_warning_time_zero(self):
        s = RoundTimerSession(_cfg(warning_time=0))
        events = _collect(s)
        s.start()
        _run_ticks(s, 10)
        warnings = [e for e in events if e.event_type == EventType.ROUND_WARNING]
        assert len(warnings) == 0

    def test_round_end_fires_after_work_duration(self):
        s = RoundTimerSession(_cfg(work_duration=3))
        events = _collect(s)
        s.start()
        events.clear()

        _run_ticks(s, 3)
        assert any(e.event_type == EventType.ROUND_END for e in events)


class TestRoundTimerSessionFullCycle:
    def test_two_rounds_full_sequence(self):
        # 2 rounds, work=2s, rest=1s, warning=1s
        s = RoundTimerSession(
            _cfg(num_rounds=2, work_duration=2, rest_duration=1, warning_time=1)
        )
        events = _collect(s)
        s.start()  # ROUND_START(1)

        s.tick()  # work elapsed=1 → WARNING(1)
        s.tick()  # work elapsed=2 → ROUND_END(1)
        # now rest
        s.tick()  # rest elapsed=1 → REST_END(1), ROUND_START(2)

        s.tick()  # work elapsed=1 → WARNING(2)
        s.tick()  # work elapsed=2 → ROUND_END(2), SESSION_END

        types = [e.event_type for e in events]
        assert types == [
            EventType.ROUND_START,  # round 1
            EventType.ROUND_WARNING,  # round 1
            EventType.ROUND_END,  # round 1
            EventType.REST_END,  # between rounds
            EventType.ROUND_START,  # round 2
            EventType.ROUND_WARNING,  # round 2
            EventType.ROUND_END,  # round 2
            EventType.SESSION_END,
        ]
        assert s.is_finished is True

    def test_single_round_no_rest(self):
        s = RoundTimerSession(
            _cfg(num_rounds=1, work_duration=2, rest_duration=0, warning_time=0)
        )
        events = _collect(s)
        s.start()
        _run_ticks(s, 2)

        types = [e.event_type for e in events]
        assert types == [
            EventType.ROUND_START,
            EventType.ROUND_END,
            EventType.SESSION_END,
        ]

    def test_zero_rest_skips_directly_to_next_round(self):
        s = RoundTimerSession(
            _cfg(num_rounds=2, work_duration=1, rest_duration=0, warning_time=0)
        )
        events = _collect(s)
        s.start()

        s.tick()  # round 1 ends, round 2 starts immediately
        s.tick()  # round 2 ends, session ends

        types = [e.event_type for e in events]
        assert types == [
            EventType.ROUND_START,  # round 1
            EventType.ROUND_END,  # round 1
            EventType.ROUND_START,  # round 2
            EventType.ROUND_END,  # round 2
            EventType.SESSION_END,
        ]

    def test_phase_remaining(self):
        s = RoundTimerSession(_cfg(work_duration=3, rest_duration=2))
        s.start()
        assert s.phase == "work"
        assert s.phase_remaining == 3

        s.tick()
        assert s.phase_remaining == 2

        s.tick()
        s.tick()  # work done, now rest
        assert s.phase == "rest"
        assert s.phase_remaining == 2

    def test_current_round_tracks_correctly(self):
        s = RoundTimerSession(
            _cfg(num_rounds=3, work_duration=1, rest_duration=1, warning_time=0)
        )
        s.start()
        assert s.current_round == 1

        s.tick()  # end round 1 → rest
        s.tick()  # end rest → round 2
        assert s.current_round == 2

        s.tick()  # end round 2 → rest
        s.tick()  # end rest → round 3
        assert s.current_round == 3


class TestRoundTimerSessionValidation:
    def test_invalid_config_raises_on_init(self):
        with pytest.raises(ValueError):
            RoundTimerSession(
                RoundTimerConfig(
                    num_rounds=0, work_duration=3, rest_duration=1, warning_time=1
                )
            )
