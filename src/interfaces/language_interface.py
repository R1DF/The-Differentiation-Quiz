# Imports
import os
import questionary
import toml
from .base import InterfaceCL
from .updates_check_interface import REPOSITORY_LINK
from utils.text import get_language_entry, break_line
from utils.system import clear, wait_for_enter

# Language interface
class LanguageInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name, dictionary_to_modify, version, current_language_name):
        self.dictionary_to_modify = dictionary_to_modify
        self.version = version
        self.languages_files = [x for x in os.listdir(os.path.join(os.getcwd(), "lang")) if x.endswith(".toml")]
        os.chdir("lang")
        self.languages_metadata = self.get_metadata_list([toml.load(x) for x in self.languages_files])
        self.languages_metadata = [x for x in self.languages_metadata if x["forVersion"] == self.version]
        self.languages_names = [x["name"] for x in self.languages_metadata]
        self.languages_names.remove(toml.load(dictionary_to_modify["defaults"]["language"])["meta"]["name"])
        os.chdir("..")
        self.dictionary_to_modify = dictionary_to_modify
        super().__init__(master, language_section_name)

    def get_metadata_list(self, metadata):
        returned = []
        for dictionary in metadata:
            if "meta" not in dictionary:
                continue
            for key in ["name", "author", "dateCreated", "description", "forVersion"]:
                if key not in dictionary["meta"]:
                    continue
            returned.append(dictionary["meta"])
        return returned


    def load_interface(self):
        # Introduction
        clear()
        print(get_language_entry(self, "languagesText"))

        # If there's no languages to change to
        match len(self.languages_files):
            case 0:
                print(get_language_entry(self, "noLanguagesText"))
                print(REPOSITORY_LINK)
                wait_for_enter(self.master.language_pack)
                return

            case 1:
                print(get_language_entry(self, "onlyOneLanguageText"))
                wait_for_enter(self.master.language_pack)
                return

        # Listing languages
        print(get_language_entry(self, "languagesInstalledText").replace("[N]", str(len(self.languages_files))))
        break_line()

        for index, language_metadata in enumerate(self.languages_metadata):
            print(f"{index + 1}. {language_metadata['name']} ({language_metadata['dateCreated']})")
            print(language_metadata["description"])
            break_line()

        # Querying languages
        query = self.languages_names.copy()
        query.append(get_language_entry(self, "cancelChoiceText"))
        files_picked_from = self.languages_files.copy()
        files_picked_from.remove(self.dictionary_to_modify["defaults"]["language"])

        try:
            new_language_file = files_picked_from[self.languages_names.index(questionary.select(
                get_language_entry(self, "changeLanguageQueryText"),
                choices=query
            ).unsafe_ask())]

            self.dictionary_to_modify["defaults"]["language"] = new_language_file

        except ValueError:  # If the option was cancelled
            pass
