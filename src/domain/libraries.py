
from .combo import Combo
from .custom_workout import CustomWorkout
from .footwork_move import FootworkMove


class ComboLibrary:
    def __init__(self) -> None:
        self._combos: list[Combo] = []

    @property
    def combos(self) -> list[Combo]:
        return list(self._combos)

    def add(self, combo: Combo) -> None:
        if any(c.name == combo.name for c in self._combos):
            raise ValueError(f"A combo named '{combo.name}' already exists.")
        self._combos.append(combo)

    def get_by_name(self, name: str) -> Combo | None:
        for combo in self._combos:
            if combo.name == name:
                return combo
        return None

    def update(self, name: str, updated: Combo) -> None:
        for i, combo in enumerate(self._combos):
            if combo.name == name:
                if updated.name != name and self.get_by_name(updated.name):
                    raise ValueError(f"A combo named '{updated.name}' already exists.")
                self._combos[i] = updated
                return
        raise KeyError(f"Combo '{name}' not found.")

    def remove(self, name: str) -> None:
        for i, combo in enumerate(self._combos):
            if combo.name == name:
                self._combos.pop(i)
                return
        raise KeyError(f"Combo '{name}' not found.")

    def list_all(self) -> list[Combo]:
        return list(self._combos)

    def __len__(self) -> int:
        return len(self._combos)

    def to_dict(self) -> list:
        return [c.to_dict() for c in self._combos]

    @classmethod
    def from_dict(cls, data: list) -> "ComboLibrary":
        lib = cls()
        for item in data:
            lib.add(Combo.from_dict(item))
        return lib


class FootworkMoveLibrary:
    def __init__(self) -> None:
        self._moves: list[FootworkMove] = []

    @property
    def moves(self) -> list[FootworkMove]:
        return list(self._moves)

    def add(self, move: FootworkMove) -> None:
        if any(m.name == move.name for m in self._moves):
            raise ValueError(f"A move named '{move.name}' already exists.")
        self._moves.append(move)

    def get_by_name(self, name: str) -> FootworkMove | None:
        for move in self._moves:
            if move.name == name:
                return move
        return None

    def update(self, name: str, updated: FootworkMove) -> None:
        for i, move in enumerate(self._moves):
            if move.name == name:
                if updated.name != name and self.get_by_name(updated.name):
                    raise ValueError(f"A move named '{updated.name}' already exists.")
                self._moves[i] = updated
                return
        raise KeyError(f"Move '{name}' not found.")

    def remove(self, name: str) -> None:
        for i, move in enumerate(self._moves):
            if move.name == name:
                self._moves.pop(i)
                return
        raise KeyError(f"Move '{name}' not found.")

    def list_all(self) -> list[FootworkMove]:
        return list(self._moves)

    def __len__(self) -> int:
        return len(self._moves)

    def to_dict(self) -> list:
        return [m.to_dict() for m in self._moves]

    @classmethod
    def from_dict(cls, data: list) -> "FootworkMoveLibrary":
        lib = cls()
        for item in data:
            lib.add(FootworkMove.from_dict(item))
        return lib


class CustomWorkoutLibrary:
    def __init__(self) -> None:
        self._workouts: list[CustomWorkout] = []

    @property
    def workouts(self) -> list[CustomWorkout]:
        return list(self._workouts)

    def add(self, workout: CustomWorkout) -> None:
        if any(w.name == workout.name for w in self._workouts):
            raise ValueError(f"A workout named '{workout.name}' already exists.")
        self._workouts.append(workout)

    def get_by_name(self, name: str) -> CustomWorkout | None:
        for workout in self._workouts:
            if workout.name == name:
                return workout
        return None

    def update(self, name: str, updated: CustomWorkout) -> None:
        for i, workout in enumerate(self._workouts):
            if workout.name == name:
                if updated.name != name and self.get_by_name(updated.name):
                    raise ValueError(
                        f"A workout named '{updated.name}' already exists."
                    )
                self._workouts[i] = updated
                return
        raise KeyError(f"Workout '{name}' not found.")

    def remove(self, name: str) -> None:
        for i, workout in enumerate(self._workouts):
            if workout.name == name:
                self._workouts.pop(i)
                return
        raise KeyError(f"Workout '{name}' not found.")

    def list_all(self) -> list[CustomWorkout]:
        return list(self._workouts)

    def __len__(self) -> int:
        return len(self._workouts)

    def to_dict(self) -> list:
        return [w.to_dict() for w in self._workouts]

    @classmethod
    def from_dict(cls, data: list) -> "CustomWorkoutLibrary":
        lib = cls()
        for item in data:
            lib.add(CustomWorkout.from_dict(item))
        return lib
