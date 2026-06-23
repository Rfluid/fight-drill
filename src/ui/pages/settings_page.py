from src.ui.page import Page


class SettingsPage(Page):
    def __init__(self, ctx):
        super().__init__(ctx)
        self._proxies = []

    def render(self) -> str:
        t = self.ctx.i18n.t
        audio_vol = int(self.ctx.app_state.audio_volume * 100)
        voice_vol = int(self.ctx.app_state.voice_volume * 100)
        voice_rate = int(self.ctx.app_state.voice_rate * 100)
        return f"""
        <div class="page-header">
            <button class="btn-back" id="btn-back">&#8592; {t("back")}</button>
            <h1>{t("settings.title")}</h1>
        </div>

        <div class="settings-section">
            <label for="slider-audio-volume">{t("home.audio_volume")}: <span id="lbl-audio-volume">{audio_vol}%</span></label>
            <input type="range" id="slider-audio-volume" min="0" max="100" value="{audio_vol}">
            <label for="slider-voice-volume">{t("home.voice_volume")}: <span id="lbl-voice-volume">{voice_vol}%</span></label>
            <input type="range" id="slider-voice-volume" min="0" max="100" value="{voice_vol}">
            <label for="slider-voice-rate">{t("home.voice_rate")}: <span id="lbl-voice-rate">{voice_rate}%</span></label>
            <input type="range" id="slider-voice-rate" min="50" max="200" step="10" value="{voice_rate}">
        </div>
        """

    def mount(self) -> None:
        from js import document  # type: ignore[import-not-found]
        from pyodide.ffi import create_proxy  # type: ignore[import-not-found]

        p = create_proxy(lambda e: self.ctx.router.navigate("#/"))
        document.getElementById("btn-back").addEventListener("click", p)
        self._proxies.append(p)

        def on_audio_volume(e):
            vol = int(e.target.value) / 100
            self.ctx.audio_engine.volume = vol
            self.ctx.app_state.audio_volume = vol
            self.ctx.app_state.save()
            document.getElementById("lbl-audio-volume").textContent = f"{int(e.target.value)}%"

        def on_voice_volume(e):
            vol = int(e.target.value) / 100
            self.ctx.announcer.volume = vol
            self.ctx.app_state.voice_volume = vol
            self.ctx.app_state.save()
            document.getElementById("lbl-voice-volume").textContent = f"{int(e.target.value)}%"

        def on_voice_rate(e):
            rate = int(e.target.value) / 100
            self.ctx.announcer.rate = rate
            self.ctx.app_state.voice_rate = rate
            self.ctx.app_state.save()
            document.getElementById("lbl-voice-rate").textContent = f"{int(e.target.value)}%"

        p_audio = create_proxy(on_audio_volume)
        p_voice = create_proxy(on_voice_volume)
        p_rate = create_proxy(on_voice_rate)
        document.getElementById("slider-audio-volume").addEventListener("input", p_audio)
        document.getElementById("slider-voice-volume").addEventListener("input", p_voice)
        document.getElementById("slider-voice-rate").addEventListener("input", p_rate)
        self._proxies.extend([p_audio, p_voice, p_rate])

    def destroy(self) -> None:
        for p in self._proxies:
            p.destroy()
