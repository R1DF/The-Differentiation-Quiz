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
        del self.current_menu  # I'm unsure if using "del" kills the class object so they aren't being redefined yet saved but whatever

    def make_game_setup_menu(self):
        self.current_menu = GameSetupInterfaceCL(self, "gameSetup")

    def make_game_loading_menu(self, difficulty):
        self.current_menu = GameLoadingInterfaceCL(self, "gameLoading", difficulty)

    def make_game_interface(self, game):
        self.current_menu = GameInterfaceCL(self, "game", game)

