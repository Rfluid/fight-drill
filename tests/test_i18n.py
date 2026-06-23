"""Tests for I18n class — locale detection fallback, translation, interpolation."""

from src.i18n import I18n


class TestI18nLocale:
    def test_defaults_to_en_without_browser(self):
        i18n = I18n()
        assert i18n.locale == "en"

    def test_explicit_locale_pt(self):
        i18n = I18n(locale="pt")
        assert i18n.locale == "pt"

    def test_explicit_locale_en(self):
        i18n = I18n(locale="en")
        assert i18n.locale == "en"

    def test_locale_setter(self):
        i18n = I18n(locale="en")
        i18n.locale = "pt"
        assert i18n.locale == "pt"


class TestI18nTranslation:
    def test_translate_pt(self):
        i18n = I18n(locale="pt")
        assert i18n.t("back") == "Voltar"
        assert i18n.t("start") == "Iniciar"
        assert i18n.t("pause") == "Pausar"
        assert i18n.t("resume") == "Continuar"
        assert i18n.t("stop") == "Parar"

    def test_translate_en(self):
        i18n = I18n(locale="en")
        assert i18n.t("back") == "Back"
        assert i18n.t("start") == "Start"
        assert i18n.t("pause") == "Pause"
        assert i18n.t("resume") == "Resume"
        assert i18n.t("stop") == "Stop"

    def test_home_page_strings_pt(self):
        i18n = I18n(locale="pt")
        assert (
            i18n.t("home.subtitle") == "Plataforma de Treinamento para Artes Marciais"
        )
        assert i18n.t("home.drills_heading") == "Modalidades de Treino"
        assert i18n.t("home.manage_heading") == "Gerenciamento"

    def test_home_page_strings_en(self):
        i18n = I18n(locale="en")
        assert i18n.t("home.subtitle") == "Martial Arts Training Platform"
        assert i18n.t("home.drills_heading") == "Training Drills"
        assert i18n.t("home.manage_heading") == "Management"

    def test_voice_announcements_pt(self):
        i18n = I18n(locale="pt")
        assert i18n.t("voice.warning") == "Atenção"
        assert i18n.t("voice.rest") == "Descanso"
        assert i18n.t("voice.session_end") == "Fim do treino"

    def test_voice_announcements_en(self):
        i18n = I18n(locale="en")
        assert i18n.t("voice.warning") == "Warning"
        assert i18n.t("voice.rest") == "Rest"
        assert i18n.t("voice.session_end") == "Workout complete"


class TestI18nInterpolation:
    def test_round_work_pt(self):
        i18n = I18n(locale="pt")
        assert i18n.t("voice.round_work", round=3) == "Round 3, trabalho"

    def test_round_work_en(self):
        i18n = I18n(locale="en")
        assert i18n.t("voice.round_work", round=5) == "Round 5, work"


class TestI18nFallback:
    def test_missing_key_in_pt_falls_back_to_en(self):
        """If a key exists in 'en' but not in 'pt', fallback to English."""
        i18n = I18n(locale="pt")
        # All keys exist in both, so test with a completely unknown key
        assert i18n.t("nonexistent_key") == "nonexistent_key"

    def test_missing_key_returns_key_itself(self):
        i18n = I18n(locale="en")
        assert i18n.t("this.does.not.exist") == "this.does.not.exist"

    def test_unknown_locale_falls_back_to_en(self):
        i18n = I18n(locale="fr")
        assert i18n.t("back") == "Back"


class TestI18nSpeechLang:
    def test_speech_lang_pt(self):
        i18n = I18n(locale="pt")
        assert i18n.speech_lang == "pt-BR"

    def test_speech_lang_en(self):
        i18n = I18n(locale="en")
        assert i18n.speech_lang == "en-US"


class TestI18nAllKeysConsistent:
    def test_pt_and_en_have_same_keys(self):
        """Both locales must define the same set of keys."""
        from src.i18n import _TRANSLATIONS

        pt_keys = set(_TRANSLATIONS["pt"].keys())
        en_keys = set(_TRANSLATIONS["en"].keys())
        assert pt_keys == en_keys, (
            f"Missing in pt: {en_keys - pt_keys}, missing in en: {pt_keys - en_keys}"
        )
