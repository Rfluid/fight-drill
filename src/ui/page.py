from abc import ABC, abstractmethod

from .app_context import AppContext


class Page(ABC):
    def __init__(self, ctx: AppContext) -> None:
        self.ctx = ctx

    @abstractmethod
    def render(self) -> str:
        """Return HTML string for this page."""
        ...

    def mount(self) -> None:
        """Bind event listeners after HTML is in the DOM."""
        pass

    def destroy(self) -> None:
        """Clean up timers, listeners, sessions before page swap."""
        pass
