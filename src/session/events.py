from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(Enum):
    ROUND_START = "round_start"
    ROUND_WARNING = "round_warning"
    ROUND_END = "round_end"
    REST_END = "rest_end"
    STIMULUS = "stimulus"
    COMBO_CALL = "combo_call"
    MOVE_CALL = "move_call"
    SESSION_END = "session_end"


@dataclass(frozen=True)
class DrillEvent:
    event_type: EventType
    data: dict[str, Any] = field(default_factory=dict)
