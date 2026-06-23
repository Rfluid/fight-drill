"""Browser-specific backends using PyScript/Pyodide js interop.

These classes are only importable inside a PyScript environment.
They implement the TonePlayer and SpeechBackend protocols.
"""


class WebAudioPlayer:
    """TonePlayer implementation using the Web Audio API."""

    def __init__(self) -> None:
        from js import window  # type: ignore[import-not-found]

        AudioContext = window.AudioContext or window.webkitAudioContext
        self._ctx = AudioContext.new()

    def play_tone(self, frequency: float, duration: float, volume: float = 1.0) -> None:
        oscillator = self._ctx.createOscillator()
        gain_node = self._ctx.createGain()

        oscillator.type = "sine"
        oscillator.frequency.setValueAtTime(frequency, self._ctx.currentTime)
        gain_node.gain.setValueAtTime(volume, self._ctx.currentTime)

        oscillator.connect(gain_node)
        gain_node.connect(self._ctx.destination)

        start_time = self._ctx.currentTime
        oscillator.start(start_time)
        oscillator.stop(start_time + duration)


class WebSpeechBackend:
    """SpeechBackend implementation using the Speech Synthesis API."""

    def __init__(self, lang: str = "en-US") -> None:
        self._lang = lang

    def speak(self, text: str, volume: float = 1.0, rate: float = 1.0) -> None:
        from js import window  # type: ignore[import-not-found]

        utterance = window.SpeechSynthesisUtterance.new(text)
        utterance.lang = self._lang
        utterance.volume = volume
        utterance.rate = rate
        window.speechSynthesis.speak(utterance)
