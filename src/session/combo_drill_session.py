import random

from src.domain.call_mode import CallMode
from src.domain.drill_config import ComboDrillConfig

from .drill_session import DrillSession
from .events import DrillEvent, EventType


class ComboDrillSession(DrillSession):
    """State machine for Combo Drill (RF03, RN02).

    Calls combos sequentially (cyclic) or randomly (no consecutive repeat).
    Emits COMBO_CALL at each interval, then SESSION_END.
    """

    def __init__(
        self,
        config: ComboDrillConfig,
        rng: random.Random | None = None,
    ) -> None:
        super().__init__(config)
        self._cfg: ComboDrillConfig = config
        self._rng = rng or random.Random()
        self._seq_index: int = 0
        self._last_called_index: int | None = None
        self._next_call_at: int = 0

    def _on_start(self) -> None:
        self._seq_index = 0
        self._last_called_index = None
        self._call_combo()
        self._next_call_at = self._elapsed + self._cfg.call_interval

    def _on_tick(self) -> None:
        if self._elapsed >= self._cfg.total_duration:
            self._emit(DrillEvent(EventType.SESSION_END))
            self.stop()
            return

        if self._elapsed >= self._next_call_at:
            self._call_combo()
            self._next_call_at = self._elapsed + self._cfg.call_interval

    def _call_combo(self) -> None:
        combo = self._pick_next()
        self._emit(
            DrillEvent(
                EventType.COMBO_CALL,
                {"combo_name": combo.name, "combo_sequence": combo.sequence},
            )
        )

    def _pick_next(self):
        combos = self._cfg.combos

        if self._cfg.call_mode == CallMode.SEQUENTIAL:
            combo = combos[self._seq_index % len(combos)]
            self._last_called_index = self._seq_index % len(combos)
            self._seq_index += 1
            return combo

        # Random mode: no consecutive repeat (RN02)
        if len(combos) == 1:
            self._last_called_index = 0
            return combos[0]

        while True:
            idx = self._rng.randint(0, len(combos) - 1)
            if idx != self._last_called_index:
                self._last_called_index = idx
                return combos[idx]
