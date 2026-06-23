"""Tests for Page.render() output — verifies HTML structure without a browser."""


from src.domain.combo import Combo
from src.domain.custom_workout import CustomWorkout
from src.domain.footwork_move import FootworkMove
from src.i18n import I18n
from src.persistence.app_state import AppState
from src.persistence.storage_manager import StorageManager
from src.ui.app_context import AppContext
from tests.fake_storage import FakeStorageBackend


class FakeAudioEngine:
    def play_start_signal(self):
        pass

    def play_warning_signal(self):
        pass

    def play_end_signal(self):
        pass


class FakeAnnouncer:
    def announce(self, text):
        pass


def _make_ctx(locale: str = "pt") -> AppContext:
    backend = FakeStorageBackend()
    storage = StorageManager(backend)
    app_state = AppState(storage)
    return AppContext(
        app_state=app_state,
        audio_engine=FakeAudioEngine(),
        announcer=FakeAnnouncer(),
        i18n=I18n(locale=locale),
    )


class TestHomePageRender:
    def test_contains_nav_cards(self):
        from src.ui.pages.home_page import HomePage

        ctx = _make_ctx()
        page = HomePage(ctx)
        html = page.render()
        assert "nav-round-timer" in html
        assert "nav-timing-drill" in html
        assert "nav-combo-drill" in html
        assert "nav-footwork-drill" in html
        assert "nav-combo-library" in html
        assert "nav-footwork-moves" in html
        assert "nav-custom-workouts" in html

    def test_contains_title(self):
        from src.ui.pages.home_page import HomePage

        ctx = _make_ctx()
        html = HomePage(ctx).render()
        assert "FightDrill" in html

    def test_has_settings_button_not_sliders(self):
        from src.ui.pages.home_page import HomePage

        ctx = _make_ctx()
        html = HomePage(ctx).render()
        assert "btn-settings" in html
        assert "slider-audio-volume" not in html


class TestSettingsPageRender:
    def test_contains_sliders(self):
        from src.ui.pages.settings_page import SettingsPage

        ctx = _make_ctx()
        html = SettingsPage(ctx).render()
        assert "slider-audio-volume" in html
        assert "slider-voice-volume" in html
        assert "slider-voice-rate" in html
        assert "btn-back" in html

    def test_en(self):
        from src.ui.pages.settings_page import SettingsPage

        ctx = _make_ctx(locale="en")
        html = SettingsPage(ctx).render()
        assert "Audio Settings" in html
        assert "Back" in html


class TestRoundTimerPageRender:
    def test_contains_config_form(self):
        from src.ui.pages.round_timer_page import RoundTimerPage

        ctx = _make_ctx()
        html = RoundTimerPage(ctx).render()
        assert "in-rounds" in html
        assert "in-work" in html
        assert "in-rest" in html
        assert "in-warning" in html
        assert "btn-start" in html

    def test_contains_running_section(self):
        from src.ui.pages.round_timer_page import RoundTimerPage

        ctx = _make_ctx()
        html = RoundTimerPage(ctx).render()
        assert "timer-display" in html
        assert "btn-pause" in html
        assert "btn-stop" in html


class TestTimingDrillPageRender:
    def test_contains_config_fields(self):
        from src.ui.pages.timing_drill_page import TimingDrillPage

        ctx = _make_ctx()
        html = TimingDrillPage(ctx).render()
        assert "in-duration" in html
        assert "in-min" in html
        assert "in-max" in html
        assert "in-technique" in html


class TestComboDrillPageRender:
    def test_empty_library_shows_message(self):
        from src.ui.pages.combo_drill_page import ComboDrillPage

        ctx = _make_ctx()
        html = ComboDrillPage(ctx).render()
        assert "Nenhum combo cadastrado" in html
        assert "btn-go-library" in html

    def test_with_combos_shows_checkboxes(self):
        from src.ui.pages.combo_drill_page import ComboDrillPage

        ctx = _make_ctx()
        ctx.app_state.combo_library.add(Combo("Combo 1", "jab, cross"))
        ctx.app_state.combo_library.add(Combo("Combo 2", "hook"))
        html = ComboDrillPage(ctx).render()
        assert "Combo 1" in html
        assert "Combo 2" in html
        assert "combo-check" in html
        assert "in-mode" in html


class TestFootworkDrillPageRender:
    def test_empty_library_shows_message(self):
        from src.ui.pages.footwork_drill_page import FootworkDrillPage

        ctx = _make_ctx()
        html = FootworkDrillPage(ctx).render()
        assert "Nenhuma movimentação cadastrada" in html

    def test_with_moves_shows_checkboxes(self):
        from src.ui.pages.footwork_drill_page import FootworkDrillPage

        ctx = _make_ctx()
        ctx.app_state.footwork_library.add(FootworkMove("lateral step"))
        html = FootworkDrillPage(ctx).render()
        assert "lateral step" in html
        assert "move-check" in html


class TestComboLibraryPageRender:
    def test_empty_shows_message(self):
        from src.ui.pages.combo_library_page import ComboLibraryPage

        ctx = _make_ctx()
        html = ComboLibraryPage(ctx).render()
        assert "Nenhum combo cadastrado" in html

    def test_with_combos_shows_items(self):
        from src.ui.pages.combo_library_page import ComboLibraryPage

        ctx = _make_ctx()
        ctx.app_state.combo_library.add(Combo("Combo 1", "jab, cross"))
        html = ComboLibraryPage(ctx).render()
        assert "Combo 1" in html
        assert "jab, cross" in html
        assert "btn-delete" in html


class TestFootworkMovePageRender:
    def test_empty_shows_message(self):
        from src.ui.pages.footwork_move_page import FootworkMovePage

        ctx = _make_ctx()
        html = FootworkMovePage(ctx).render()
        assert "Nenhuma movimentação cadastrada" in html

    def test_with_moves_shows_items(self):
        from src.ui.pages.footwork_move_page import FootworkMovePage

        ctx = _make_ctx()
        ctx.app_state.footwork_library.add(FootworkMove("retreat"))
        html = FootworkMovePage(ctx).render()
        assert "retreat" in html


class TestCustomWorkoutPageRender:
    def test_empty_shows_message(self):
        from src.ui.pages.custom_workout_page import CustomWorkoutPage

        ctx = _make_ctx()
        html = CustomWorkoutPage(ctx).render()
        assert "Nenhum treino personalizado" in html

    def test_with_workouts_shows_items(self):
        from src.ui.pages.custom_workout_page import CustomWorkoutPage

        ctx = _make_ctx()
        ctx.app_state.workout_library.add(CustomWorkout("Shadow", 300, "3 rounds"))
        html = CustomWorkoutPage(ctx).render()
        assert "Shadow" in html
        assert "5min 0s" in html
        assert "3 rounds" in html


# --- i18n locale tests: verify pages render with English locale ---


class TestPagesRenderEnglish:
    def test_home_page_en(self):
        from src.ui.pages.home_page import HomePage

        ctx = _make_ctx(locale="en")
        html = HomePage(ctx).render()
        assert "Martial Arts Training Platform" in html
        assert "Training Drills" in html
        assert "Management" in html

    def test_round_timer_page_en(self):
        from src.ui.pages.round_timer_page import RoundTimerPage

        ctx = _make_ctx(locale="en")
        html = RoundTimerPage(ctx).render()
        assert "Back" in html
        assert "Start" in html
        assert "Work (s)" in html
        assert "Rest (s)" in html

    def test_combo_drill_empty_en(self):
        from src.ui.pages.combo_drill_page import ComboDrillPage

        ctx = _make_ctx(locale="en")
        html = ComboDrillPage(ctx).render()
        assert "No combos registered" in html
        assert "Go to Combo Library" in html

    def test_footwork_drill_empty_en(self):
        from src.ui.pages.footwork_drill_page import FootworkDrillPage

        ctx = _make_ctx(locale="en")
        html = FootworkDrillPage(ctx).render()
        assert "No footwork moves registered" in html

    def test_combo_library_empty_en(self):
        from src.ui.pages.combo_library_page import ComboLibraryPage

        ctx = _make_ctx(locale="en")
        html = ComboLibraryPage(ctx).render()
        assert "No combos registered" in html
        assert "Combo Library" in html

    def test_footwork_move_empty_en(self):
        from src.ui.pages.footwork_move_page import FootworkMovePage

        ctx = _make_ctx(locale="en")
        html = FootworkMovePage(ctx).render()
        assert "No footwork moves registered" in html
        assert "Footwork Moves" in html

    def test_custom_workout_empty_en(self):
        from src.ui.pages.custom_workout_page import CustomWorkoutPage

        ctx = _make_ctx(locale="en")
        html = CustomWorkoutPage(ctx).render()
        assert "No custom workouts registered" in html
        assert "Custom Workouts" in html

    def test_timing_drill_page_en(self):
        from src.ui.pages.timing_drill_page import TimingDrillPage

        ctx = _make_ctx(locale="en")
        html = TimingDrillPage(ctx).render()
        assert "Total duration (s)" in html
        assert "Target technique" in html
