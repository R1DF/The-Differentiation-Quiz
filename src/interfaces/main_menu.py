# Imports
import questionary
import sys
from .base import InterfaceCL
from utils.text import get_language_entry, get_language_confirmation, break_line
from utils.system import clear


# Main menu
class MainMenuInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name):
        super().__init__(master, language_section_name)

    def load_interface(self):
        clear()
        print(get_language_entry(self, "welcomeText"))
        print(get_language_entry(self, "runningVersionText").replace("[VERSION]", self.master.VERSION))
        break_line()

        options_choices = get_language_entry(self, "doWhatQueryChoices")
        selected_option = options_choices.index(questionary.select(
            get_language_entry(self, "doWhatQueryText"),
            choices=options_choices
        ).unsafe_ask())

        match selected_option:
            case 0:
                self.master.make_game_setup_menu()
                return

            case 1:
                self.master.make_settings_interface()
                return

            case 2:
                self.master.make_updates_check_interface()
                return

            case 3:
                break_line()
                if get_language_confirmation(self, "confirmQuitQuery"):
                    sys.exit()

        self.load_interface()  # If the code doesn't break up from there then the menu will re-load

