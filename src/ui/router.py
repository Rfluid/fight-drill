from collections.abc import Callable

from .page import Page

PageFactory = Callable[[], Page]


class Router:
    """Hash-based SPA router.

    In the browser, call start() to begin listening for hashchange events.
    In tests, call navigate() directly.
    """

    def __init__(self, container_id: str = "app") -> None:
        self._routes: dict[str, PageFactory] = {}
        self._container_id = container_id
        self._current_page: Page | None = None
        self._proxy = None

    def register(self, path: str, factory: PageFactory) -> None:
        self._routes[path] = factory

    def resolve(self, hash_str: str) -> PageFactory | None:
        path = hash_str.lstrip("#") or "/"
        if not path.startswith("/"):
            path = "/" + path
        return self._routes.get(path)

    def start(self) -> None:
        """Start listening for hash changes (browser only)."""
        from js import window  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        self._proxy = create_proxy(lambda e: self._render_current())
        window.addEventListener("hashchange", self._proxy)
        self._render_current()

    def navigate(self, path: str) -> None:
        from js import window  # type: ignore[import-not-found]

        window.location.hash = path

    def _render_current(self) -> None:
        from js import document, window  # type: ignore[import-not-found]

        hash_str = str(window.location.hash)
        factory = self.resolve(hash_str)
        if factory is None:
            window.location.hash = "#/"
            return

        if self._current_page is not None:
            self._current_page.destroy()

        page = factory()
        self._current_page = page
        container = document.getElementById(self._container_id)
        container.innerHTML = page.render()
        page.mount()
