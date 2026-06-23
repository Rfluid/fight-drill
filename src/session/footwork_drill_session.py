import random

from src.domain.drill_config import FootworkDrillConfig

from .drill_session import DrillSession
from .events import DrillEvent, EventType


class FootworkDrillSession(DrillSession):
    """State machine for Footwork Drill (RF04, RN05).

    Calls random footwork moves at random intervals within the configured range.
    Emits MOVE_CALL at each stimulus, then SESSION_END.
    """

    def __init__(
        self,
        config: FootworkDrillConfig,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(config)
        self._cfg: FootworkDrillConfig = config
        self._rng = rng or random.Random()
        self._next_call_at: int = 0

    def _schedule_next(self) -> None:
        delay = self._rng.randint(self._cfg.min_interval, self._cfg.max_interval)
        self._next_call_at = self._elapsed + delay

    def _on_start(self) -> None:
        self._call_move()
        self._schedule_next()

    def _on_tick(self) -> None:
        if self._elapsed >= self._cfg.total_duration:
            self._emit(DrillEvent(EventType.SESSION_END))
            self.stop()
            return

        if self._elapsed >= self._next_call_at:
            self._call_move()
            self._schedule_next()

    def _call_move(self) -> None:
        move = self._rng.choice(self._cfg.moves)
        self._emit(
            DrillEvent(
                EventType.MOVE_CALL,
                {"move_name": move.name},
            )
        )
