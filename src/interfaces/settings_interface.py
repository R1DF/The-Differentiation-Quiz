# Imports
import questionary
import copy
import toml
import os
from .base import InterfaceCL
from utils.text import get_language_entry, get_utility_entry, warn, break_line
from utils.system import clear, wait_for_enter


# Settings interface
class SettingsInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name):
        self.original_settings = master.configurations.data.copy()  # Getting settings and putting them apart
        self.current_settings = copy.deepcopy(self.original_settings)
        super().__init__(master, language_section_name)

    def load_interface(self):
        # Introduction
        clear()
        print(get_language_entry(self, "settingsIntroductionText"))
        current_language = toml.load(os.path.join("lang", self.current_settings["defaults"]["language"]))["meta"][
            "name"]
        break_line()

        # Printing out the current settings
        for entry, key in (("verifyFilePresenceText", "verify_file_presence"), ("safeStartText", "safe_start")):
            print(get_language_entry(self, entry), end=" ")
            print(get_utility_entry(self.master, "closedQuestionAnswers")[not self.current_settings['program'][key]])

        print(get_language_entry(self, "languageText"), current_language)
        break_line()

        # Checking saved changes
        if self.original_settings != self.current_settings:
            warn(get_language_entry(self, "unsavedChangesText"))
            break_line()

        # Getting choices
        choices = [
                      get_language_entry(self,
                                         f"{'dontV' if self.current_settings['program']['verify_file_presence'] else 'v'}erifyFilePresenceChoiceText"),
                      get_language_entry(self,
                                         f"{'dontS' if self.current_settings['program']['safe_start'] else 's'}tartSafelyChoiceText"),
                  ] + get_language_entry(self, "settingsOptionEntries")
        choice = choices.index(questionary.select(
            get_language_entry(self, "selectOptionQueryText"),
            choices=choices
        ).unsafe_ask())
        break_line()

        # Acting on choices
        match choice:
            case 0:
                self.current_settings["program"]["verify_file_presence"] = not self.current_settings["program"][
                    "verify_file_presence"]

            case 1:
                self.current_settings["program"]["safe_start"] = not self.current_settings["program"]["safe_start"]

            case 2:
                clear()
                self.master.make_language_interface(self.current_settings)

            case 3:
                print(get_language_entry(self, "creditsText"))
                wait_for_enter(self.master.language_pack)

            case 4:
                if self.current_settings != self.original_settings:
                    toml.dump(self.current_settings, open(os.path.join("config", "conf.toml"), "w"))
                    print(get_language_entry(self, "restartNeededText"))
                else:
                    print(get_language_entry(self, "sameSettingsText"))
                wait_for_enter(self.master.language_pack, True)
                self.master.make_main_menu()
                return

            case 5:
                self.master.make_main_menu()
                return

        self.load_interface()

