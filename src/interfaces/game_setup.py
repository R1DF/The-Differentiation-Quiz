# Imports
import questionary
import sys
from .base import InterfaceCL
from utils.text import get_language_entry, combine_language_entries, get_language_confirmation, break_line
from utils.system import clear

# Main menu
class GameSetupInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name):
        super().__init__(master, language_section_name)

    def load_interface(self):
        clear()
        print(get_language_entry(self, "difficultiesText"))
        print(combine_language_entries(
            self,
            *[f"{x}DifficultyDescription" for x in ("easy", "medium", "hard")]
        ))
        break_line()

        options_choices = get_language_entry(self, "difficultiesQueryChoices")
        selected_option = options_choices.index(questionary.select(
            get_language_entry(self, "difficultiesQueryText"),
            choices=options_choices
        ).unsafe_ask())

        match selected_option:
            case 3:
                self.master.make_main_menu()
                return

        self.load_interface()

