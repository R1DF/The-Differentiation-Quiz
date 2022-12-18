# Imports
import colorama

# Simple coloured text functions
def success(prompt = "", end="\n"):
    print(colorama.Fore.GREEN + prompt + colorama.Style.RESET_ALL, end=end)

def warn(prompt = "", end="\n"):
    print(colorama.Fore.YELLOW + prompt + colorama.Style.RESET_ALL, end=end)

def alarm(prompt = "", end="\n"):
    print(colorama.Fore.RED + prompt + colorama.Style.RESET_ALL, end=end)

def notify(prompt = "", end="\n"):
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
