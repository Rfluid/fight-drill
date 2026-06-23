from collections.abc import Callable

from src.audio.audio_engine import AudioEngine
from src.session.drill_session import DrillSession

COUNTDOWN_SECONDS = 3


class DrillTimer:
    """Wraps browser setInterval to tick a DrillSession every second."""

    def __init__(
        self,
        session: DrillSession,
        on_tick: Callable[[], None],
        on_countdown: Callable[[int], None] | None = None,
        audio_engine: AudioEngine | None = None,
    ) -> None:
        self._session = session
        self._on_tick = on_tick
        self._on_countdown = on_countdown
        self._audio = audio_engine
        self._interval_id: int | None = None
        self._proxy = None
        self._countdown_remaining: int = 0
        self._in_countdown: bool = False

    def start(self) -> None:
        from js import window  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        self._countdown_remaining = COUNTDOWN_SECONDS
        self._in_countdown = True

        if self._on_countdown:
            self._on_countdown(self._countdown_remaining)

        def _countdown_tick():
            self._countdown_remaining -= 1
            if self._countdown_remaining > 0:
                if self._audio:
                    self._audio.play_countdown_tick_signal()
                if self._on_countdown:
                    self._on_countdown(self._countdown_remaining)
            else:
                self._in_countdown = False
                self._clear_interval()
                self._session.start()
                if self._audio:
                    self._audio.play_countdown_end_signal()
                if self._on_countdown:
                    self._on_countdown(0)

                def _tick():
                    self._session.tick()
                    self._on_tick()

                self._proxy = create_proxy(_tick)
                self._interval_id = window.setInterval(self._proxy, 1000)

        self._proxy = create_proxy(_countdown_tick)
        self._interval_id = window.setInterval(self._proxy, 1000)

    def pause(self) -> None:
        if not self._in_countdown:
            self._session.pause()

    def resume(self) -> None:
        if not self._in_countdown:
            self._session.resume()

    def stop(self) -> None:
        self._in_countdown = False
        self._clear_interval()
        self._session.stop()
        if self._proxy is not None:
            self._proxy.destroy()
            self._proxy = None

    def _clear_interval(self) -> None:
        if self._interval_id is not None:
            from js import window  # type: ignore[import-not-found]

            window.clearInterval(self._interval_id)
            self._interval_id = None
