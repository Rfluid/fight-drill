from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class SignalType(Enum):
    START = "start"
    WARNING = "warning"
    END = "end"
    COUNTDOWN_TICK = "countdown_tick"
    COUNTDOWN_END = "countdown_end"


@dataclass(frozen=True)
class ToneSpec:
    frequency: float  # Hz
    duration: float  # seconds
    volume: float = 1.0  # 0.0 to 1.0


# Default signal definitions
SIGNAL_TONES: dict[SignalType, list[ToneSpec]] = {
    SignalType.START: [
        ToneSpec(frequency=800, duration=0.3),
    ],
    SignalType.WARNING: [
        ToneSpec(frequency=500, duration=0.15),
        ToneSpec(frequency=500, duration=0.15),
        ToneSpec(frequency=500, duration=0.15),
    ],
    SignalType.END: [
        ToneSpec(frequency=1000, duration=0.5),
        ToneSpec(frequency=600, duration=0.5),
    ],
    SignalType.COUNTDOWN_TICK: [
        ToneSpec(frequency=480, duration=0.08),
    ],
    SignalType.COUNTDOWN_END: [
        ToneSpec(frequency=880, duration=0.15),
        ToneSpec(frequency=1100, duration=0.25),
    ],
}


class TonePlayer(Protocol):
    """Protocol for the low-level tone playback backend.

    In the browser this is implemented via Web Audio API.
    In tests this is replaced by a mock/fake.
    """

    def play_tone(self, frequency: float, duration: float, volume: float) -> None: ...


class AudioEngine:
    """Plays structured audio signals for drill events.

    Delegates actual sound output to a TonePlayer backend,
    keeping signal logic testable without a browser.
    """

    def __init__(
        self,
        player: TonePlayer,
        signals: dict[SignalType, list[ToneSpec]] | None = None,
    ) -> None:
        self._player = player
        self._signals = signals if signals is not None else dict(SIGNAL_TONES)
        self._volume: float = 1.0

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._volume = max(0.0, min(1.0, value))

    def play_tone(self, frequency: float, duration: float, volume: float = 1.0) -> None:
        self._player.play_tone(frequency, duration, volume * self._volume)

    def play_signal(self, signal_type: SignalType) -> None:
        tones = self._signals.get(signal_type, [])
        for tone in tones:
            self._player.play_tone(tone.frequency, tone.duration, tone.volume * self._volume)

    def play_start_signal(self) -> None:
        self.play_signal(SignalType.START)

    def play_warning_signal(self) -> None:
        self.play_signal(SignalType.WARNING)

    def play_end_signal(self) -> None:
        self.play_signal(SignalType.END)

    def play_countdown_tick_signal(self) -> None:
        self.play_signal(SignalType.COUNTDOWN_TICK)

    def play_countdown_end_signal(self) -> None:
        self.play_signal(SignalType.COUNTDOWN_END)

    def get_signal_tones(self, signal_type: SignalType) -> list[ToneSpec]:
        return list(self._signals.get(signal_type, []))

    def set_signal_tones(self, signal_type: SignalType, tones: list[ToneSpec]) -> None:
        self._signals[signal_type] = list(tones)
