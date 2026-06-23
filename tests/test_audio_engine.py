import pytest

from src.audio.audio_engine import SIGNAL_TONES, AudioEngine, SignalType, ToneSpec


class FakeTonePlayer:
    """Records all play_tone calls for assertion."""

    def __init__(self) -> None:
        self.calls: list[tuple[float, float, float]] = []

    def play_tone(self, frequency: float, duration: float, volume: float) -> None:
        self.calls.append((frequency, duration, volume))


class TestToneSpec:
    def test_defaults(self):
        spec = ToneSpec(frequency=440, duration=0.5)
        assert spec.frequency == 440
        assert spec.duration == 0.5
        assert spec.volume == 1.0

    def test_custom_volume(self):
        spec = ToneSpec(frequency=440, duration=0.5, volume=0.5)
        assert spec.volume == 0.5

    def test_immutable(self):
        spec = ToneSpec(frequency=440, duration=0.5)
        with pytest.raises(AttributeError):
            spec.frequency = 880  # type: ignore[misc]


class TestSignalTones:
    def test_all_signal_types_have_defaults(self):
        for signal_type in SignalType:
            assert signal_type in SIGNAL_TONES
            assert len(SIGNAL_TONES[signal_type]) > 0


class TestAudioEngine:
    def test_play_tone_delegates_to_player(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        engine.play_tone(440, 0.5, 0.8)
        assert player.calls == [(440, 0.5, 0.8)]

    def test_play_tone_default_volume(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        engine.play_tone(440, 0.5)
        assert player.calls == [(440, 0.5, 1.0)]

    def test_play_start_signal(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        engine.play_start_signal()
        expected = SIGNAL_TONES[SignalType.START]
        assert len(player.calls) == len(expected)
        for call, spec in zip(player.calls, expected):
            assert call == (spec.frequency, spec.duration, spec.volume)

    def test_play_warning_signal(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        engine.play_warning_signal()
        expected = SIGNAL_TONES[SignalType.WARNING]
        assert len(player.calls) == len(expected)

    def test_play_end_signal(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        engine.play_end_signal()
        expected = SIGNAL_TONES[SignalType.END]
        assert len(player.calls) == len(expected)

    def test_custom_signals(self):
        player = FakeTonePlayer()
        custom = {SignalType.START: [ToneSpec(1000, 1.0)]}
        engine = AudioEngine(player, signals=custom)
        engine.play_start_signal()
        assert player.calls == [(1000, 1.0, 1.0)]

    def test_custom_signals_do_not_affect_defaults(self):
        player = FakeTonePlayer()
        custom = {SignalType.START: [ToneSpec(1000, 1.0)]}
        engine = AudioEngine(player, signals=custom)
        # WARNING and END should produce nothing since they're not in custom
        engine.play_warning_signal()
        assert player.calls == []

    def test_get_signal_tones(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        tones = engine.get_signal_tones(SignalType.START)
        assert tones == SIGNAL_TONES[SignalType.START]

    def test_get_signal_tones_returns_copy(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        tones = engine.get_signal_tones(SignalType.START)
        tones.clear()
        assert len(engine.get_signal_tones(SignalType.START)) > 0

    def test_set_signal_tones(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        new_tones = [ToneSpec(200, 0.1)]
        engine.set_signal_tones(SignalType.START, new_tones)
        engine.play_start_signal()
        assert player.calls == [(200, 0.1, 1.0)]

    def test_set_signal_tones_stores_copy(self):
        player = FakeTonePlayer()
        engine = AudioEngine(player)
        new_tones = [ToneSpec(200, 0.1)]
        engine.set_signal_tones(SignalType.START, new_tones)
        new_tones.clear()
        assert len(engine.get_signal_tones(SignalType.START)) == 1

    def test_play_signal_unknown_type_does_nothing(self):
        player = FakeTonePlayer()
        custom = {SignalType.START: [ToneSpec(800, 0.3)]}
        engine = AudioEngine(player, signals=custom)
        engine.play_signal(SignalType.END)
        assert player.calls == []
