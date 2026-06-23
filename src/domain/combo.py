from dataclasses import dataclass


@dataclass
class Combo:
    name: str
    sequence: str

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        self.sequence = self.sequence.strip()
        if not self.name:
            raise ValueError("Combo name must not be empty.")

    def to_dict(self) -> dict:
        return {"name": self.name, "sequence": self.sequence}

    @classmethod
    def from_dict(cls, data: dict) -> "Combo":
        return cls(name=data["name"], sequence=data["sequence"])
