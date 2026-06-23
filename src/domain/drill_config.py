from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .call_mode import CallMode
from .combo import Combo
from .footwork_move import FootworkMove


class DrillConfig(ABC):
    @abstractmethod
    def validate(self) -> None: ...

    @abstractmethod
    def to_dict(self) -> dict: ...


@dataclass
class RoundTimerConfig(DrillConfig):
    num_rounds: int
    work_duration: int  # seconds
    rest_duration: int  # seconds
    warning_time: int  # seconds before round end

    def validate(self) -> None:
        if self.num_rounds <= 0:
            raise ValueError("Number of rounds must be greater than zero.")
        if self.work_duration <= 0:
            raise ValueError("Work duration must be greater than zero.")
        if self.rest_duration < 0:
            raise ValueError("Rest duration must not be negative.")
        if self.warning_time < 0:
            raise ValueError("Warning time must not be negative.")
        if self.warning_time >= self.work_duration:
            raise ValueError("Warning time must be less than work duration.")

    def to_dict(self) -> dict:
        return {
            "type": "round_timer",
            "num_rounds": self.num_rounds,
            "work_duration": self.work_duration,
            "rest_duration": self.rest_duration,
            "warning_time": self.warning_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RoundTimerConfig":
        return cls(
            num_rounds=data["num_rounds"],
            work_duration=data["work_duration"],
            rest_duration=data["rest_duration"],
            warning_time=data["warning_time"],
        )


@dataclass
class TimingDrillConfig(DrillConfig):
    total_duration: int  # seconds
    min_interval: int  # seconds
    max_interval: int  # seconds
    target_technique: str

    def validate(self) -> None:
        if self.total_duration <= 0:
            raise ValueError("Total duration must be greater than zero.")
        if self.min_interval <= 0:
            raise ValueError("Minimum interval must be greater than zero.")
        if self.min_interval >= self.max_interval:
            raise ValueError(
                "Minimum interval must be strictly less than maximum interval."
            )
        if not self.target_technique.strip():
            raise ValueError("Target technique must not be empty.")

    def to_dict(self) -> dict:
        return {
            "type": "timing_drill",
            "total_duration": self.total_duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "target_technique": self.target_technique,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimingDrillConfig":
        return cls(
            total_duration=data["total_duration"],
            min_interval=data["min_interval"],
            max_interval=data["max_interval"],
            target_technique=data["target_technique"],
        )


@dataclass
class ComboDrillConfig(DrillConfig):
    combos: list[Combo] = field(default_factory=list)
    call_mode: CallMode = CallMode.SEQUENTIAL
    call_interval: int = 5  # seconds
    total_duration: int = 180  # seconds

    def validate(self) -> None:
        if not self.combos:
            raise ValueError("At least one combo must be selected.")
        if self.call_interval <= 0:
            raise ValueError("Call interval must be greater than zero.")
        if self.total_duration <= 0:
            raise ValueError("Total duration must be greater than zero.")

    def to_dict(self) -> dict:
        return {
            "type": "combo_drill",
            "combos": [c.to_dict() for c in self.combos],
            "call_mode": self.call_mode.value,
            "call_interval": self.call_interval,
            "total_duration": self.total_duration,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ComboDrillConfig":
        return cls(
            combos=[Combo.from_dict(c) for c in data["combos"]],
            call_mode=CallMode(data["call_mode"]),
            call_interval=data["call_interval"],
            total_duration=data["total_duration"],
        )


@dataclass
class FootworkDrillConfig(DrillConfig):
    moves: list[FootworkMove] = field(default_factory=list)
    min_interval: int = 2  # seconds
    max_interval: int = 5  # seconds
    total_duration: int = 180  # seconds

    def validate(self) -> None:
        if not self.moves:
            raise ValueError("At least one footwork move must be selected.")
        if self.min_interval <= 0:
            raise ValueError("Minimum interval must be greater than zero.")
        if self.min_interval >= self.max_interval:
            raise ValueError(
                "Minimum interval must be strictly less than maximum interval."
            )
        if self.total_duration <= 0:
            raise ValueError("Total duration must be greater than zero.")

    def to_dict(self) -> dict:
        return {
            "type": "footwork_drill",
            "moves": [m.to_dict() for m in self.moves],
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "total_duration": self.total_duration,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FootworkDrillConfig":
        return cls(
            moves=[FootworkMove.from_dict(m) for m in data["moves"]],
            min_interval=data["min_interval"],
            max_interval=data["max_interval"],
            total_duration=data["total_duration"],
        )
