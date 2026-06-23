from dataclasses import dataclass


@dataclass
class FootworkMove:
    name: str

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Footwork move name must not be empty.")

    def to_dict(self) -> dict:
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "FootworkMove":
        return cls(name=data["name"])
