# Imports
import requests
from .base import InterfaceCL
from utils.text import get_language_entry, success, warn, alarm, break_line
from utils.system import clear, wait_for_enter


# Constants
TEST_URL = "http://httpstat.us/200"
VERSION_CHECK_URL = "https://r1df.github.io/version_check.json"
UPDATES_LINK = "https://github.com/R1DF/The-Differentiation-Quiz/releases"


# Updates check interface
class UpdatesCheckInterface(InterfaceCL):
    def __init__(self, master, language_section_name, version):
        self.version = version
        super().__init__(master, language_section_name)

    def check_version(self):
        # Testing connection
        print(get_language_entry(self, "testingSampleRequestText"))
        try:
            requests.get(TEST_URL)
        except requests.exceptions.ConnectionError:
            alarm(get_language_entry(self, "noInternetErrorText"))
            return
        success(get_language_entry(self, "requestPassedText"))
        break_line()

        # Connecting to website
        print(get_language_entry(self, "checkingForUpdatesText"))
        try:
            response = requests.get(VERSION_CHECK_URL)
        except requests.exceptions.ConnectionError:
            alarm(get_language_entry(self, "noInternetErrorText"))
            return

        # Getting status code and handling exceptions
        if response.status_code != 200:
            alarm(get_language_entry(self, "invalidStatusCodeText").replace("[CODE]", str(response.status_code)))
            break_line()

            print(get_language_entry(self, "linkToCheckText"))
            print(UPDATES_LINK)
            return

        version_data = response.json()["tdq"]
        if self.version != version_data["v"]:
            warn(get_language_entry(self, "upgradeNeededText").replace(
                "[OLD]", self.version).replace(
                "[NEW]", version_data["v"]
            ))

            if note := version_data["note"]:
                break_line()
                print(get_language_entry(self, "versionNotesIntroducerText"))
                print(note)
            break_line()

            print(get_language_entry(self, "getUpdatesLinkText"))
            print(UPDATES_LINK)
        else:
            success(get_language_entry(self, "latestVersionText"))

    def load_interface(self):
        clear()
        self.check_version()
        break_line()

        wait_for_enter(self.master.language_pack)
        self.master.make_main_menu()

