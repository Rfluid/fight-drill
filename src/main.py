"""FightDrill — Entry point for PyScript."""

from src.audio.announcer import Announcer
from src.audio.audio_engine import AudioEngine
from src.audio.web_backends import WebAudioPlayer, WebSpeechBackend
from src.i18n import I18n
from src.persistence.app_state import AppState
from src.persistence.storage_manager import StorageManager
from src.persistence.web_backend import LocalStorageBackend
from src.ui.app_context import AppContext
from src.ui.pages import (
    ComboDrillPage,
    ComboLibraryPage,
    CustomWorkoutPage,
    FootworkDrillPage,
    FootworkMovePage,
    HomePage,
    RoundTimerPage,
    SettingsPage,
    TimingDrillPage,
)
from src.ui.router import Router

# --- i18n ---

i18n = I18n()

# --- Bootstrap ---

storage = StorageManager(LocalStorageBackend())
app_state = AppState(storage)
loaded = app_state.load()

audio_engine = AudioEngine(WebAudioPlayer())
announcer = Announcer(WebSpeechBackend(lang=i18n.speech_lang))

audio_engine.volume = app_state.audio_volume
announcer.volume = app_state.voice_volume
announcer.rate = app_state.voice_rate

router = Router("app")
ctx = AppContext(
    app_state=app_state,
    audio_engine=audio_engine,
    announcer=announcer,
    i18n=i18n,
    router=router,
)

# --- Set HTML lang ---

from js import document as js_doc  # type: ignore[import-not-found]

js_doc.documentElement.lang = i18n.speech_lang

# --- Routes ---

router.register("/", lambda: HomePage(ctx))
router.register("/round-timer", lambda: RoundTimerPage(ctx))
router.register("/timing-drill", lambda: TimingDrillPage(ctx))
router.register("/combo-drill", lambda: ComboDrillPage(ctx))
router.register("/footwork-drill", lambda: FootworkDrillPage(ctx))
router.register("/combo-library", lambda: ComboLibraryPage(ctx))
router.register("/footwork-moves", lambda: FootworkMovePage(ctx))
router.register("/custom-workouts", lambda: CustomWorkoutPage(ctx))
router.register("/settings", lambda: SettingsPage(ctx))

# --- Start ---

if not loaded and app_state.load_error:
    from js import window  # type: ignore[import-not-found]

    window.alert(f"{i18n.t('alert.corrupt_data')}\n\n{app_state.load_error}")

router.start()
