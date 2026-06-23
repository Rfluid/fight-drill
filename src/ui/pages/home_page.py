from src.ui.page import Page


class HomePage(Page):
    def render(self) -> str:
        t = self.ctx.i18n.t
        return f"""
        <div class="home-header">
            <h1>FightDrill</h1>
            <button class="btn-config" id="btn-settings" title="{t("settings.title")}">&#9881;</button>
        </div>
        <p class="subtitle">{t("home.subtitle")}</p>

        <h2>{t("home.drills_heading")}</h2>
        <div class="card-grid">
            <button class="nav-card" id="nav-round-timer">
                <span class="card-icon">&#9201;</span>
                <span class="card-title">Round Timer</span>
                <span class="card-desc">{t("home.round_timer_desc")}</span>
            </button>
            <button class="nav-card" id="nav-timing-drill">
                <span class="card-icon">&#9889;</span>
                <span class="card-title">Timing Drill</span>
                <span class="card-desc">{t("home.timing_drill_desc")}</span>
            </button>
            <button class="nav-card" id="nav-combo-drill">
                <span class="card-icon">&#9994;</span>
                <span class="card-title">Combo Drill</span>
                <span class="card-desc">{t("home.combo_drill_desc")}</span>
            </button>
            <button class="nav-card" id="nav-footwork-drill">
                <span class="card-icon">&#128095;</span>
                <span class="card-title">Footwork Drill</span>
                <span class="card-desc">{t("home.footwork_drill_desc")}</span>
            </button>
        </div>

        <h2>{t("home.manage_heading")}</h2>
        <div class="card-grid">
            <button class="nav-card nav-card--manage" id="nav-combo-library">
                <span class="card-title">{t("home.combo_library")}</span>
            </button>
            <button class="nav-card nav-card--manage" id="nav-footwork-moves">
                <span class="card-title">{t("home.footwork_moves")}</span>
            </button>
            <button class="nav-card nav-card--manage" id="nav-custom-workouts">
                <span class="card-title">{t("home.custom_workouts")}</span>
            </button>
        </div>
        """

    def mount(self) -> None:
        from js import document  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        routes = {
            "nav-round-timer": "#/round-timer",
            "nav-timing-drill": "#/timing-drill",
            "nav-combo-drill": "#/combo-drill",
            "nav-footwork-drill": "#/footwork-drill",
            "nav-combo-library": "#/combo-library",
            "nav-footwork-moves": "#/footwork-moves",
            "nav-custom-workouts": "#/custom-workouts",
            "btn-settings": "#/settings",
        }
        self._proxies = []
        for elem_id, path in routes.items():
            proxy = create_proxy(lambda e, p=path: self.ctx.router.navigate(p))
            document.getElementById(elem_id).addEventListener("click", proxy)
            self._proxies.append(proxy)

    def destroy(self) -> None:
        if hasattr(self, "_proxies"):
            for p in self._proxies:
                p.destroy()
