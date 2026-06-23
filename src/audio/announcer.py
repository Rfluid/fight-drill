from typing import Protocol


class SpeechBackend(Protocol):
    """Protocol for text-to-speech playback.

    In the browser this is implemented via the Speech Synthesis API.
    In tests this is replaced by a mock/fake.
    """

    def speak(self, text: str, volume: float = 1.0, rate: float = 1.0) -> None: ...


class Announcer:
    """Announces combo/move names via voice synthesis (RN06).

    Delegates actual speech output to a SpeechBackend,
    keeping announcement logic testable without a browser.
    """

    def __init__(self, backend: SpeechBackend) -> None:
        self._backend = backend
        self._enabled = True
        self._volume: float = 1.0
        self._rate: float = 1.0

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._volume = max(0.0, min(1.0, value))

    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(self, value: float) -> None:
        self._rate = max(0.1, min(4.0, value))

    def announce(self, text: str) -> None:
        if not self._enabled:
            return
        cleaned = text.strip()
        if not cleaned:
            return
        self._backend.speak(cleaned, self._volume, self._rate)
