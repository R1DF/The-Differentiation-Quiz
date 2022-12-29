"""
The Differentiation Quiz (17.12.22)
Coded by R1DF.
View licence at LICENCE.md.

Please run start.py if you want to play via source.
"""

# Imports
from interfaces.main_menu import MainMenuInterfaceCL
from interfaces.game_setup import GameSetupInterfaceCL
from interfaces.game_loader import GameLoadingInterfaceCL
from interfaces.game_interface import GameInterfaceCL
from interfaces.updates_check_interface import UpdatesCheckInterfaceCL
from interfaces.settings_interface import SettingsInterfaceCL
from interfaces.language_interface import LanguageInterfaceCL
from utils.system import title
from config_loader import Configurations
from lang_loader import LanguagePack


# App
class TheDifferentiationQuiz:
    VERSION = "1.0.0"

    def __init__(self, configurations: Configurations, language_pack: LanguagePack):
        self.configurations = configurations
        self.language_pack = language_pack
        title(f"The Differentiation Quiz [{TheDifferentiationQuiz.VERSION}]")
        self.current_menu = None
        self.make_main_menu()

    def make_main_menu(self):
        self.current_menu = MainMenuInterfaceCL(self, "mainMenu")
        del self.current_menu  # I'm unsure if using "del" kills the class object, so they aren't being redefined yet saved but whatever

    def make_game_setup_menu(self):
        self.current_menu = GameSetupInterfaceCL(self, "gameSetup")
        del self.current_menu

    def make_game_loading_menu(self, difficulty):
        self.current_menu = GameLoadingInterfaceCL(self, "gameLoading", difficulty)
        del self.current_menu

    def make_game_interface(self, game):
        self.current_menu = GameInterfaceCL(self, "game", game)
        del self.current_menu

    def make_updates_check_interface(self):
        self.current_menu = UpdatesCheckInterfaceCL(self, "checkingUpdates", TheDifferentiationQuiz.VERSION)
        del self.current_menu

    def make_settings_interface(self):
        self.current_menu = SettingsInterfaceCL(self, "settings")
        del self.current_menu

    def make_language_interface(self, dictionary_to_modify):
        self.current_menu = LanguageInterfaceCL(self, "language", dictionary_to_modify, TheDifferentiationQuiz.VERSION)
        # del self.current_menu  # Unneeded

