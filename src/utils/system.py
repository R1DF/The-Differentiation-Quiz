# Imports
import os
import platform
import readchar

# Platform
PLATFORM = platform.system()

# System functions
def title(terminal_title=""):
    # Only works for windows
    if PLATFORM == "Windows":
        os.system(f"title {terminal_title}")


def wait(language_pack, to_exit=False):
    print(language_pack.section_get("multipleUse")["pressToExit" if to_exit else "pressToContinue"])


def wait_for_enter(language_pack, to_exit=False):
    print(language_pack.section_get("multipleUse")["enterToExit" if to_exit else "enterToContinue"])
    while True:
        if readchar.readkey() == readchar.key.ENTER:
            break


def clear():
    os.system("cls" if PLATFORM == "Windows" else "clear")

