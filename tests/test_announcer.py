from src.audio.announcer import Announcer


class FakeSpeechBackend:
    """Records all speak calls for assertion."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, float, float]] = []

    def speak(self, text: str, volume: float = 1.0, rate: float = 1.0) -> None:
        self.calls.append((text, volume, rate))


class TestAnnouncer:
    def test_announce_delegates_to_backend(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("Combo 1")
        assert backend.calls == [("Combo 1", 1.0, 1.0)]

    def test_announce_strips_whitespace(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("  lateral step  ")
        assert backend.calls == [("lateral step", 1.0, 1.0)]

    def test_announce_empty_string_ignored(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("")
        assert backend.calls == []

    def test_announce_whitespace_only_ignored(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("   ")
        assert backend.calls == []

    def test_announce_disabled(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.enabled = False
        announcer.announce("Combo 1")
        assert backend.calls == []

    def test_announce_re_enabled(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.enabled = False
        announcer.announce("Combo 1")
        announcer.enabled = True
        announcer.announce("Combo 2")
        assert backend.calls == [("Combo 2", 1.0, 1.0)]

    def test_enabled_default_true(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        assert announcer.enabled is True

    def test_multiple_announcements(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.announce("jab")
        announcer.announce("cross")
        announcer.announce("hook")
        assert backend.calls == [("jab", 1.0, 1.0), ("cross", 1.0, 1.0), ("hook", 1.0, 1.0)]

    def test_volume_default_is_one(self):
        announcer = Announcer(FakeSpeechBackend())
        assert announcer.volume == 1.0

    def test_volume_passed_to_backend(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.volume = 0.5
        announcer.announce("jab")
        assert backend.calls == [("jab", 0.5, 1.0)]

    def test_volume_clamped_to_zero(self):
        announcer = Announcer(FakeSpeechBackend())
        announcer.volume = -0.5
        assert announcer.volume == 0.0

    def test_volume_clamped_to_one(self):
        announcer = Announcer(FakeSpeechBackend())
        announcer.volume = 1.5
        assert announcer.volume == 1.0

    def test_rate_default_is_one(self):
        announcer = Announcer(FakeSpeechBackend())
        assert announcer.rate == 1.0

    def test_rate_passed_to_backend(self):
        backend = FakeSpeechBackend()
        announcer = Announcer(backend)
        announcer.rate = 1.5
        announcer.announce("jab")
        assert backend.calls == [("jab", 1.0, 1.5)]

    def test_rate_clamped_to_min(self):
        announcer = Announcer(FakeSpeechBackend())
        announcer.rate = 0.0
        assert announcer.rate == 0.1

    def test_rate_clamped_to_max(self):
        announcer = Announcer(FakeSpeechBackend())
        announcer.rate = 5.0
        assert announcer.rate == 4.0
