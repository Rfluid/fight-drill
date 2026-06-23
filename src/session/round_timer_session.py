from enum import Enum

from src.domain.drill_config import RoundTimerConfig

from .drill_session import DrillSession
from .events import DrillEvent, EventType


class _Phase(Enum):
    WORK = "work"
    REST = "rest"


class RoundTimerSession(DrillSession):
    """State machine for Round Timer (RF01).

    Cycles through work/rest phases for the configured number of rounds.
    Emits ROUND_START, ROUND_WARNING, ROUND_END, REST_END, SESSION_END.
    """

    def __init__(self, config: RoundTimerConfig) -> None:
        super().__init__(config)
        self._cfg: RoundTimerConfig = config
        self._current_round: int = 0
        self._phase: _Phase = _Phase.WORK
        self._phase_elapsed: int = 0
        self._warning_fired: bool = False

    @property
    def current_round(self) -> int:
        return self._current_round

    @property
    def phase(self) -> str:
        return self._phase.value

    @property
    def phase_remaining(self) -> int:
        if self._phase == _Phase.WORK:
            return max(0, self._cfg.work_duration - self._phase_elapsed)
        return max(0, self._cfg.rest_duration - self._phase_elapsed)

    def _on_start(self) -> None:
        self._current_round = 1
        self._phase = _Phase.WORK
        self._phase_elapsed = 0
        self._warning_fired = False
        self._emit(DrillEvent(EventType.ROUND_START, {"round": 1}))

    def _on_tick(self) -> None:
        self._phase_elapsed += 1

        if self._phase == _Phase.WORK:
            self._tick_work()
        else:
            self._tick_rest()

    def _tick_work(self) -> None:
        time_remaining = self._cfg.work_duration - self._phase_elapsed

        if (
            not self._warning_fired
            and self._cfg.warning_time > 0
            and time_remaining <= self._cfg.warning_time
            and time_remaining >= 0
        ):
            self._warning_fired = True
            self._emit(
                DrillEvent(
                    EventType.ROUND_WARNING,
                    {"round": self._current_round},
                )
            )

        if self._phase_elapsed >= self._cfg.work_duration:
            self._emit(
                DrillEvent(
                    EventType.ROUND_END,
                    {"round": self._current_round},
                )
            )

            if self._current_round >= self._cfg.num_rounds:
                self._emit(DrillEvent(EventType.SESSION_END))
                self.stop()
                return

            if self._cfg.rest_duration > 0:
                self._phase = _Phase.REST
                self._phase_elapsed = 0
            else:
                self._start_next_round()

    def _tick_rest(self) -> None:
        if self._phase_elapsed >= self._cfg.rest_duration:
            self._emit(
                DrillEvent(
                    EventType.REST_END,
                    {"round": self._current_round},
                )
            )
            self._start_next_round()

    def _start_next_round(self) -> None:
        self._current_round += 1
        self._phase = _Phase.WORK
        self._phase_elapsed = 0
        self._warning_fired = False
        self._emit(
            DrillEvent(
                EventType.ROUND_START,
                {"round": self._current_round},
            )
        )
