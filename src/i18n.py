"""Internationalization (i18n) — supports pt-BR and en."""

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "pt": {
        # -- Home page --
        "home.subtitle": "Plataforma de Treinamento para Artes Marciais",
        "home.drills_heading": "Modalidades de Treino",
        "home.manage_heading": "Gerenciamento",
        "home.round_timer_desc": "Rounds de trabalho e descanso",
        "home.timing_drill_desc": "Reação a estímulo aleatório",
        "home.combo_drill_desc": "Chamadas de combos",
        "home.footwork_drill_desc": "Movimentação e deslocamento",
        "home.combo_library": "Biblioteca de Combos",
        "home.footwork_moves": "Movimentações",
        "home.custom_workouts": "Treinos Personalizados",
        "home.settings_heading": "Configurações de Áudio",
        "home.audio_volume": "Volume dos beeps",
        "home.voice_volume": "Volume da voz",
        "home.voice_rate": "Velocidade da voz",
        # -- Settings --
        "settings.title": "Configurações de Áudio",
        # -- Common --
        "back": "Voltar",
        "start": "Iniciar",
        "pause": "Pausar",
        "resume": "Continuar",
        "stop": "Parar",
        "add": "Adicionar",
        "delete": "Excluir",
        # -- Round Timer --
        "round_timer.title": "Round Timer",
        "round_timer.rounds": "Rounds",
        "round_timer.work_s": "Trabalho (s)",
        "round_timer.rest_s": "Descanso (s)",
        "round_timer.warning_s": "Aviso antes do fim (s)",
        "round_timer.phase_work": "TRABALHO",
        "round_timer.phase_rest": "DESCANSO",
        # -- Timing Drill --
        "timing_drill.title": "Timing Drill",
        "timing_drill.duration_s": "Duração total (s)",
        "timing_drill.min_interval_s": "Intervalo mínimo (s)",
        "timing_drill.max_interval_s": "Intervalo máximo (s)",
        "timing_drill.target_technique": "Técnica-alvo",
        "timing_drill.target_placeholder": "ex: jab, teep",
        # -- Combo Drill --
        "combo_drill.title": "Combo Drill",
        "combo_drill.no_combos": "Nenhum combo cadastrado.",
        "combo_drill.go_library": "Ir para Biblioteca de Combos",
        "combo_drill.select_combos": "Selecione os combos",
        "combo_drill.call_mode": "Modo de chamada",
        "combo_drill.mode_sequential": "Sequencial",
        "combo_drill.mode_random": "Aleatório",
        "combo_drill.interval_s": "Intervalo entre chamadas (s)",
        "combo_drill.duration_s": "Duração total (s)",
        # -- Footwork Drill --
        "footwork_drill.title": "Footwork Drill",
        "footwork_drill.no_moves": "Nenhuma movimentação cadastrada.",
        "footwork_drill.go_moves": "Ir para Movimentações",
        "footwork_drill.select_moves": "Selecione as movimentações",
        "footwork_drill.min_interval_s": "Intervalo mínimo (s)",
        "footwork_drill.max_interval_s": "Intervalo máximo (s)",
        "footwork_drill.duration_s": "Duração total (s)",
        # -- Combo Library --
        "combo_library.title": "Biblioteca de Combos",
        "combo_library.name": "Nome",
        "combo_library.name_placeholder": "ex: Combo 1",
        "combo_library.sequence": "Sequência de técnicas",
        "combo_library.sequence_placeholder": "ex: jab, cross, hook",
        "combo_library.empty": "Nenhum combo cadastrado.",
        # -- Footwork Moves --
        "footwork_move.title": "Movimentações (Footwork)",
        "footwork_move.name": "Nome da movimentação",
        "footwork_move.name_placeholder": "ex: passo lateral direito",
        "footwork_move.empty": "Nenhuma movimentação cadastrada.",
        # -- Custom Workouts --
        "custom_workout.title": "Treinos Personalizados",
        "custom_workout.name": "Nome",
        "custom_workout.name_placeholder": "ex: Shadow Boxing",
        "custom_workout.duration_s": "Duração (segundos)",
        "custom_workout.description": "Descrição (opcional)",
        "custom_workout.desc_placeholder": "Instruções, observações...",
        "custom_workout.empty": "Nenhum treino personalizado cadastrado.",
        # -- Countdown --
        "countdown": "PREPARE-SE",
        # -- Voice announcements --
        "voice.round_work": "Round {round}, trabalho",
        "voice.warning": "Atenção",
        "voice.rest": "Descanso",
        "voice.session_end": "Fim do treino",
        # -- Alerts --
        "alert.corrupt_data": "Dados corrompidos no localStorage. Estado resetado.",
        # -- Loading --
        "loading": "Carregando FightDrill...",
    },
    "en": {
        # -- Home page --
        "home.subtitle": "Martial Arts Training Platform",
        "home.drills_heading": "Training Drills",
        "home.manage_heading": "Management",
        "home.round_timer_desc": "Work and rest rounds",
        "home.timing_drill_desc": "Random stimulus reaction",
        "home.combo_drill_desc": "Combo calls",
        "home.footwork_drill_desc": "Movement and footwork",
        "home.combo_library": "Combo Library",
        "home.footwork_moves": "Footwork Moves",
        "home.custom_workouts": "Custom Workouts",
        "home.settings_heading": "Audio Settings",
        "home.audio_volume": "Beep volume",
        "home.voice_volume": "Voice volume",
        "home.voice_rate": "Voice speed",
        # -- Settings --
        "settings.title": "Audio Settings",
        # -- Common --
        "back": "Back",
        "start": "Start",
        "pause": "Pause",
        "resume": "Resume",
        "stop": "Stop",
        "add": "Add",
        "delete": "Delete",
        # -- Round Timer --
        "round_timer.title": "Round Timer",
        "round_timer.rounds": "Rounds",
        "round_timer.work_s": "Work (s)",
        "round_timer.rest_s": "Rest (s)",
        "round_timer.warning_s": "Warning before end (s)",
        "round_timer.phase_work": "WORK",
        "round_timer.phase_rest": "REST",
        # -- Timing Drill --
        "timing_drill.title": "Timing Drill",
        "timing_drill.duration_s": "Total duration (s)",
        "timing_drill.min_interval_s": "Minimum interval (s)",
        "timing_drill.max_interval_s": "Maximum interval (s)",
        "timing_drill.target_technique": "Target technique",
        "timing_drill.target_placeholder": "e.g.: jab, teep",
        # -- Combo Drill --
        "combo_drill.title": "Combo Drill",
        "combo_drill.no_combos": "No combos registered.",
        "combo_drill.go_library": "Go to Combo Library",
        "combo_drill.select_combos": "Select combos",
        "combo_drill.call_mode": "Call mode",
        "combo_drill.mode_sequential": "Sequential",
        "combo_drill.mode_random": "Random",
        "combo_drill.interval_s": "Interval between calls (s)",
        "combo_drill.duration_s": "Total duration (s)",
        # -- Footwork Drill --
        "footwork_drill.title": "Footwork Drill",
        "footwork_drill.no_moves": "No footwork moves registered.",
        "footwork_drill.go_moves": "Go to Footwork Moves",
        "footwork_drill.select_moves": "Select footwork moves",
        "footwork_drill.min_interval_s": "Minimum interval (s)",
        "footwork_drill.max_interval_s": "Maximum interval (s)",
        "footwork_drill.duration_s": "Total duration (s)",
        # -- Combo Library --
        "combo_library.title": "Combo Library",
        "combo_library.name": "Name",
        "combo_library.name_placeholder": "e.g.: Combo 1",
        "combo_library.sequence": "Technique sequence",
        "combo_library.sequence_placeholder": "e.g.: jab, cross, hook",
        "combo_library.empty": "No combos registered.",
        # -- Footwork Moves --
        "footwork_move.title": "Footwork Moves",
        "footwork_move.name": "Move name",
        "footwork_move.name_placeholder": "e.g.: lateral step right",
        "footwork_move.empty": "No footwork moves registered.",
        # -- Custom Workouts --
        "custom_workout.title": "Custom Workouts",
        "custom_workout.name": "Name",
        "custom_workout.name_placeholder": "e.g.: Shadow Boxing",
        "custom_workout.duration_s": "Duration (seconds)",
        "custom_workout.description": "Description (optional)",
        "custom_workout.desc_placeholder": "Instructions, notes...",
        "custom_workout.empty": "No custom workouts registered.",
        # -- Countdown --
        "countdown": "GET READY",
        # -- Voice announcements --
        "voice.round_work": "Round {round}, work",
        "voice.warning": "Warning",
        "voice.rest": "Rest",
        "voice.session_end": "Workout complete",
        # -- Alerts --
        "alert.corrupt_data": "Corrupt data in localStorage. State has been reset.",
        # -- Loading --
        "loading": "Loading FightDrill...",
    },
}


class I18n:
    """Manages translations for pt-BR and en locales."""

    def __init__(self, locale: str | None = None) -> None:
        if locale is None:
            locale = self.detect_locale()
        self._locale = locale

    @property
    def locale(self) -> str:
        return self._locale

    @locale.setter
    def locale(self, value: str) -> None:
        self._locale = value

    @staticmethod
    def detect_locale() -> str:
        """Detect locale from browser navigator.language. Falls back to 'en'."""
        try:
            from js import navigator  # type: ignore[import-not-found]

            lang = str(navigator.language)
            if lang.startswith("pt"):
                return "pt"
        except ImportError:
            pass
        return "en"

    def t(self, key: str, **kwargs: object) -> str:
        """Return translated string for *key*, with optional interpolation.

        Falls back to English if key is missing in the active locale.
        Returns the key itself if not found in either locale.
        """
        translations = _TRANSLATIONS.get(self._locale, {})
        text = translations.get(key)
        if text is None:
            text = _TRANSLATIONS["en"].get(key)
        if text is None:
            return key
        if kwargs:
            text = text.format(**kwargs)
        return text

    @property
    def speech_lang(self) -> str:
        """BCP-47 language tag for the Speech Synthesis API."""
        return "pt-BR" if self._locale == "pt" else "en-US"
