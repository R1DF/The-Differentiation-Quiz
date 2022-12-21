# Imports
import colorama
import questionary


# Simple coloured text functions
def success(prompt="", end="\n"):
    print(colorama.Fore.GREEN + prompt + colorama.Style.RESET_ALL, end=end)


def warn(prompt="", end="\n"):
    print(colorama.Fore.YELLOW + prompt + colorama.Style.RESET_ALL, end=end)


def alarm(prompt="", end="\n"):
    print(colorama.Fore.RED + prompt + colorama.Style.RESET_ALL, end=end)


def notify(prompt="", end="\n"):
    print(colorama.Fore.BLUE + prompt + colorama.Style.RESET_ALL, end=end)


def print_c(prompt, end="\n"):
    # C for "coloured"
    replacement_tuple = (
        ("R#", colorama.Fore.RED),
        ("B#", colorama.Fore.BLUE),
        ("Y#", colorama.Fore.YELLOW),
        ("G#", colorama.Fore.GREEN),
        ("M#", colorama.Fore.MAGENTA),
        ("C#", colorama.Fore.CYAN),
        ("~|", colorama.Style.RESET_ALL)
    )
    for replaced, replacer in replacement_tuple:
        prompt = prompt.replace(replaced, replacer)
    print(prompt, end=end)


# Language specific functions. (They must be called within print() to be outputted)
def get_language_entry(interface, entry):
    # Used for each one-line print statement of an entry from a language pack
    return interface.language_section[entry]


def combine_language_entries(interface, *entries):
    # Used to avoid multiple print statements for several entries of a language pack at once.
    return "\n".join([interface.language_section[entry] for entry in entries])


def get_alienated_entry(master, menu, entry):
    # get_language_entry() but called when text from another menu section is needed.
    return master.language_pack.menu_get(menu)[entry]


def get_utility_entry(master, entry):
    # get_language_entry() but used for text in the multipleUse area.
    return master.language_pack.section_get("multipleUse")[entry]


def get_language_confirmation(interface, entry):
    # Asks a yes/no confirmation question.
    close_ended_answers = get_utility_entry(interface.master, "closedQuestionAnswers")
    return not close_ended_answers.index(questionary.select(
        get_language_entry(interface, entry),
        choices=close_ended_answers
    ).ask())


# Simple functions non-language dependent
def break_line(amount=1):
    print("\n" * (amount - 1))

