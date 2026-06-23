from src.ui.router import Router


class FakePage:
    def __init__(self, name: str):
        self.name = name

    def render(self) -> str:
        return f"<div>{self.name}</div>"

    def mount(self) -> None:
        pass

    def destroy(self) -> None:
        pass


class TestRouterResolve:
    def test_resolve_root(self):
        r = Router()
        r.register("/", lambda: FakePage("home"))
        factory = r.resolve("#/")
        assert factory is not None
        assert factory().name == "home"

    def test_resolve_empty_hash(self):
        r = Router()
        r.register("/", lambda: FakePage("home"))
        factory = r.resolve("")
        assert factory is not None
        assert factory().name == "home"

    def test_resolve_hash_only(self):
        r = Router()
        r.register("/", lambda: FakePage("home"))
        factory = r.resolve("#")
        assert factory is not None

    def test_resolve_named_route(self):
        r = Router()
        r.register("/round-timer", lambda: FakePage("timer"))
        factory = r.resolve("#/round-timer")
        assert factory is not None
        assert factory().name == "timer"

    def test_resolve_unknown_returns_none(self):
        r = Router()
        r.register("/", lambda: FakePage("home"))
        assert r.resolve("#/nonexistent") is None

    def test_multiple_routes(self):
        r = Router()
        r.register("/", lambda: FakePage("home"))
        r.register("/a", lambda: FakePage("a"))
        r.register("/b", lambda: FakePage("b"))
        assert r.resolve("#/a")().name == "a"
        assert r.resolve("#/b")().name == "b"
        assert r.resolve("#/")().name == "home"
