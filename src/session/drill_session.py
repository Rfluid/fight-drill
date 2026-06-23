from abc import ABC, abstractmethod
from collections.abc import Callable

from src.domain.drill_config import DrillConfig

from .events import DrillEvent

EventCallback = Callable[[DrillEvent], None]


class DrillSession(ABC):
    """Abstract base for all drill session state machines.

    Subclasses implement `tick()` which is called once per second.
    Events are emitted via registered callbacks.
    """

    def __init__(self, config: DrillConfig) -> None:
        config.validate()
        self._config = config
        self._elapsed: int = 0  # seconds
        self._is_running: bool = False
        self._is_paused: bool = False
        self._is_finished: bool = False
        self._callbacks: list[EventCallback] = []

    @property
    def config(self) -> DrillConfig:
        return self._config

    @property
    def elapsed(self) -> int:
        return self._elapsed

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    def on_event(self, callback: EventCallback) -> None:
        self._callbacks.append(callback)

    def _emit(self, event: DrillEvent) -> None:
        for cb in self._callbacks:
            cb(event)

    def start(self) -> None:
        if self._is_finished:
            return
        self._is_running = True
        self._is_paused = False
        self._on_start()

    def pause(self) -> None:
        if self._is_running and not self._is_paused:
            self._is_paused = True

    def resume(self) -> None:
        if self._is_running and self._is_paused:
            self._is_paused = False

    def stop(self) -> None:
        self._is_running = False
        self._is_paused = False
        self._is_finished = True

    def tick(self) -> None:
        if not self._is_running or self._is_paused or self._is_finished:
            return
        self._elapsed += 1
        self._on_tick()

    @abstractmethod
    def _on_start(self) -> None:
        """Called once when the session starts."""
        ...

    @abstractmethod
    def _on_tick(self) -> None:
        """Called every second while running."""
        ...
