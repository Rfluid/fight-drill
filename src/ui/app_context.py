from dataclasses import dataclass

from src.audio.announcer import Announcer
from src.audio.audio_engine import AudioEngine
from src.i18n import I18n
from src.persistence.app_state import AppState


@dataclass
class AppContext:
    app_state: AppState
    audio_engine: AudioEngine
    announcer: Announcer
    i18n: I18n
    router: "object | None" = None  # set after Router is created
