import random

from src.domain.drill_config import TimingDrillConfig

from .drill_session import DrillSession
from .events import DrillEvent, EventType


class TimingDrillSession(DrillSession):
    """State machine for Timing Drill (RF02).

    Emits STIMULUS at random intervals within the configured range,
    then SESSION_END when total duration is reached.
    """

    def __init__(
        self,
        config: TimingDrillConfig,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(config)
        self._cfg: TimingDrillConfig = config
        self._rng = rng or random.Random()
        self._next_stimulus_at: int = 0

    def _schedule_next(self) -> None:
        delay = self._rng.randint(self._cfg.min_interval, self._cfg.max_interval)
        self._next_stimulus_at = self._elapsed + delay

    def _on_start(self) -> None:
        self._schedule_next()

    def _on_tick(self) -> None:
        if self._elapsed >= self._cfg.total_duration:
            self._emit(DrillEvent(EventType.SESSION_END))
            self.stop()
            return

        if self._elapsed >= self._next_stimulus_at:
            self._emit(
                DrillEvent(
                    EventType.STIMULUS,
                    {"technique": self._cfg.target_technique},
                )
            )
            self._schedule_next()
