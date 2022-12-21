"""
The Differentiation Quiz (17.12.22)
Coded by R1DF.
View licence at LICENCE.md.

Please run start.py if you want to play via source.
"""

# Imports
from interfaces.main_menu import MainMenuInterfaceCL
from utils.system import title, clear
from config_loader import Configurations
from lang_loader import LanguagePack

# App
class TheDifferentiationQuiz:
    VERSION = "1.0.0"
    def __init__(self, configurations: Configurations, language_pack: LanguagePack):
        self.configurations = configurations
        self.language_pack = language_pack
        title(f"The Differentiation Quiz [{TheDifferentiationQuiz.VERSION}]")
        self.main_menu = MainMenuInterfaceCL(self, "mainMenu")
