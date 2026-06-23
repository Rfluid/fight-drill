from dataclasses import dataclass


@dataclass
class CustomWorkout:
    """A custom workout suggested by a coach (RN04)."""

    name: str
    duration: int  # seconds
    description: str = ""

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.description = self.description.strip()
        if not self.name:
            raise ValueError("Workout name must not be empty.")
        if self.duration <= 0:
            raise ValueError("Workout duration must be greater than zero.")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "duration": self.duration,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CustomWorkout":
        return cls(
            name=data["name"],
            duration=data["duration"],
            description=data.get("description", ""),
        )
