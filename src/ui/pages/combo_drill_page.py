from src.domain.call_mode import CallMode
from src.domain.drill_config import ComboDrillConfig
from src.session.combo_drill_session import ComboDrillSession
from src.session.events import DrillEvent, EventType
from src.ui.drill_timer import DrillTimer
from src.ui.page import Page


def _fmt_time(seconds: int) -> str:
    m, s = divmod(max(0, seconds), 60)
    return f"{m:02d}:{s:02d}"


class ComboDrillPage(Page):
    def __init__(self, ctx):
        super().__init__(ctx)
        self._timer: DrillTimer | None = None
        self._session: ComboDrillSession | None = None
        self._proxies = []

    def render(self) -> str:
        t = self.ctx.i18n.t
        combos = self.ctx.app_state.combo_library.list_all()

        if not combos:
            return f"""
            <div class="page-header">
                <button class="btn-back" id="btn-back">&#8592; {t("back")}</button>
                <h1>{t("combo_drill.title")}</h1>
            </div>
            <div class="empty-state">
                <p>{t("combo_drill.no_combos")}</p>
                <button class="btn-primary" id="btn-go-library">{t("combo_drill.go_library")}</button>
            </div>
            """

        combo_checkboxes = ""
        for i, c in enumerate(combos):
            combo_checkboxes += f"""
            <label class="checkbox-label">
                <input type="checkbox" class="combo-check" value="{i}" checked>
                {c.name} — <em>{c.sequence}</em>
            </label>
            """

        return f"""
        <div class="page-header">
            <button class="btn-back" id="btn-back">&#8592; {t("back")}</button>
            <h1>{t("combo_drill.title")}</h1>
        </div>

        <div id="config-section" class="config-form">
            <fieldset>
                <legend>{t("combo_drill.select_combos")}</legend>
                {combo_checkboxes}
            </fieldset>
            <label>{t("combo_drill.call_mode")}
                <select id="in-mode">
                    <option value="sequential">{t("combo_drill.mode_sequential")}</option>
                    <option value="random">{t("combo_drill.mode_random")}</option>
                </select>
            </label>
            <label>{t("combo_drill.interval_s")}
                <input type="number" id="in-interval" value="5" min="1">
            </label>
            <label>{t("combo_drill.duration_s")}
                <input type="number" id="in-duration" value="180" min="1">
            </label>
            <button class="btn-primary" id="btn-start">{t("start")}</button>
            <p id="config-error" class="error-msg"></p>
        </div>

        <div id="running-section" class="running-display" style="display:none;">
            <div class="timer-display" id="timer-display">00:00</div>
            <div class="combo-display">
                <div class="combo-name" id="combo-name">-</div>
                <div class="combo-sequence" id="combo-sequence"></div>
            </div>
            <div class="timer-controls">
                <button class="btn-secondary" id="btn-pause">{t("pause")}</button>
                <button class="btn-danger" id="btn-stop">{t("stop")}</button>
            </div>
        </div>
        """

    def mount(self) -> None:
        from js import document  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        p = create_proxy(lambda e: self.ctx.router.navigate("#/"))
        document.getElementById("btn-back").addEventListener("click", p)
        self._proxies.append(p)

        btn_library = document.getElementById("btn-go-library")
        if btn_library:
            p = create_proxy(lambda e: self.ctx.router.navigate("#/combo-library"))
            btn_library.addEventListener("click", p)
            self._proxies.append(p)
            return

        p = create_proxy(lambda e: self._on_start())
        document.getElementById("btn-start").addEventListener("click", p)
        self._proxies.append(p)

        p = create_proxy(lambda e: self._on_pause())
        document.getElementById("btn-pause").addEventListener("click", p)
        self._proxies.append(p)

        p = create_proxy(lambda e: self._on_stop())
        document.getElementById("btn-stop").addEventListener("click", p)
        self._proxies.append(p)

    def destroy(self) -> None:
        if self._timer:
            self._timer.stop()
        for p in self._proxies:
            p.destroy()

    def _on_start(self) -> None:
        from js import document  # type: ignore[import-not-found]

        combos = self.ctx.app_state.combo_library.list_all()
        checkboxes = document.querySelectorAll(".combo-check")
        selected = []
        for cb in checkboxes:
            if cb.checked:
                selected.append(combos[int(cb.value)])

        try:
            mode = CallMode(document.getElementById("in-mode").value)
            config = ComboDrillConfig(
                combos=selected,
                call_mode=mode,
                call_interval=int(document.getElementById("in-interval").value),
                total_duration=int(document.getElementById("in-duration").value),
            )
            config.validate()
        except (ValueError, TypeError) as e:
            document.getElementById("config-error").textContent = str(e)
            return

        document.getElementById("config-section").style.display = "none"
        document.getElementById("running-section").style.display = ""

        self._total = config.total_duration
        self._session = ComboDrillSession(config)
        self._session.on_event(self._handle_event)
        self._timer = DrillTimer(
            self._session, self._update_display, self._on_countdown,
            audio_engine=self.ctx.audio_engine,
        )
        self._timer.start()

    def _on_countdown(self, remaining: int) -> None:
        from js import document  # type: ignore[import-not-found]

        display = document.getElementById("timer-display")
        if remaining > 0:
            display.textContent = str(remaining)
        else:
            display.textContent = _fmt_time(self._total)

    def _on_pause(self) -> None:
        from js import document  # type: ignore[import-not-found]

        t = self.ctx.i18n.t
        if not self._timer or not self._session:
            return
        if self._session.is_paused:
            self._timer.resume()
            document.getElementById("btn-pause").textContent = t("pause")
        else:
            self._timer.pause()
            document.getElementById("btn-pause").textContent = t("resume")

    def _on_stop(self) -> None:
        if self._timer:
            self._timer.stop()
        self._show_config()

    def _handle_event(self, event: DrillEvent) -> None:
        from js import document  # type: ignore[import-not-found]

        if event.event_type == EventType.COMBO_CALL:
            self.ctx.audio_engine.play_start_signal()
            self.ctx.announcer.announce(event.data["combo_name"])
            document.getElementById("combo-name").textContent = event.data["combo_name"]
            document.getElementById("combo-sequence").textContent = event.data[
                "combo_sequence"
            ]
        elif event.event_type == EventType.SESSION_END:
            self.ctx.audio_engine.play_end_signal()
            self.ctx.announcer.announce(self.ctx.i18n.t("voice.session_end"))
            self._show_config()

    def _update_display(self) -> None:
        from js import document  # type: ignore[import-not-found]

        if not self._session:
            return
        remaining = max(0, self._total - self._session.elapsed)
        document.getElementById("timer-display").textContent = _fmt_time(remaining)

    def _show_config(self) -> None:
        from js import document  # type: ignore[import-not-found]

        document.getElementById("config-section").style.display = ""
        document.getElementById("running-section").style.display = "none"
