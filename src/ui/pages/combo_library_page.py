from src.domain.combo import Combo
from src.ui.page import Page


class ComboLibraryPage(Page):
    def __init__(self, ctx):
        super().__init__(ctx)
        self._proxies = []

    def render(self) -> str:
        t = self.ctx.i18n.t
        combos = self.ctx.app_state.combo_library.list_all()
        rows = ""
        for c in combos:
            rows += f"""
            <div class="library-item" data-name="{c.name}">
                <div class="item-info">
                    <strong>{c.name}</strong>
                    <span>{c.sequence}</span>
                </div>
                <div class="item-actions">
                    <button class="btn-small btn-danger btn-delete" data-name="{c.name}">{t("delete")}</button>
                </div>
            </div>
            """

        empty_msg = (
            f'<p class="empty-msg">{t("combo_library.empty")}</p>' if not combos else ""
        )

        return f"""
        <div class="page-header">
            <button class="btn-back" id="btn-back">&#8592; {t("back")}</button>
            <h1>{t("combo_library.title")}</h1>
        </div>

        <div class="config-form add-form">
            <label>{t("combo_library.name")}
                <input type="text" id="in-name" placeholder="{t("combo_library.name_placeholder")}">
            </label>
            <label>{t("combo_library.sequence")}
                <input type="text" id="in-sequence" placeholder="{t("combo_library.sequence_placeholder")}">
            </label>
            <button class="btn-primary" id="btn-add">{t("add")}</button>
            <p id="form-error" class="error-msg"></p>
        </div>

        <div class="library-list" id="library-list">
            {empty_msg}
            {rows}
        </div>
        """

    def mount(self) -> None:
        from js import document  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        p = create_proxy(lambda e: self.ctx.router.navigate("#/"))
        document.getElementById("btn-back").addEventListener("click", p)
        self._proxies.append(p)

        p = create_proxy(lambda e: self._on_add())
        document.getElementById("btn-add").addEventListener("click", p)
        self._proxies.append(p)

        self._bind_delete_buttons()

    def destroy(self) -> None:
        for p in self._proxies:
            p.destroy()

    def _bind_delete_buttons(self) -> None:
        from js import document  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        for btn in document.querySelectorAll(".btn-delete"):
            name = btn.getAttribute("data-name")
            p = create_proxy(lambda e, n=name: self._on_delete(n))
            btn.addEventListener("click", p)
            self._proxies.append(p)

    def _on_add(self) -> None:
        from js import document  # type: ignore[import-not-found]

        name = document.getElementById("in-name").value.strip()
        sequence = document.getElementById("in-sequence").value.strip()

        try:
            combo = Combo(name=name, sequence=sequence)
            self.ctx.app_state.combo_library.add(combo)
            self.ctx.app_state.save()
        except ValueError as e:
            document.getElementById("form-error").textContent = str(e)
            return

        self._rerender()

    def _on_delete(self, name: str) -> None:
        self.ctx.app_state.combo_library.remove(name)
        self.ctx.app_state.save()
        self._rerender()

    def _rerender(self) -> None:
        from js import document  # type: ignore[import-not-found]

        for p in self._proxies:
            p.destroy()
        self._proxies.clear()

        container = document.getElementById("app")
        container.innerHTML = self.render()
        self.mount()
