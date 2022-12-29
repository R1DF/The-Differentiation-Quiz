# Attempting imports
try:
    import colorama
    import sys
    import os
    import platform
    import readchar
    from config_loader import Configurations
    from lang_loader import LanguagePack
    from main import TheDifferentiationQuiz
    from verifier import Verifier
    colorama.init()

    clear = lambda: os.system("cls" if platform.system() == "Windows" else "clear")

    configurations = Configurations(os.path.join("config", "conf.toml"))
    language = LanguagePack(os.path.join("lang", configurations.defaults["language"]))

except (ModuleNotFoundError, ImportError) as exception:
    print(f"An error occurred while running the program:\n"
          f"{'Could not locate a necessary module to import.' if type(exception).__name__ == 'ModuleNotFoundError' else 'Could not import a class or function.'}\n"
          f"Exception message: {exception} [{type(exception).__name__}]\n\n"
          f"Please reinstall the game.\n"
          f"[LANGUAGE DEFAULTED TO ENGLISH]\n")
    sys.exit()


# Starts
def safe_start():
    # Safe start handles exceptions.
    try:
        TheDifferentiationQuiz(configurations, language)  # Starts the program
    except Exception as unprecedented_exception:
        if platform.system() == "Windows":
            os.system("title The Differentiation Quiz: Error")
        section = language.section_get("exceptionHandling")
        print("\n".join((
            section["errorHappenedText"],
            section["exceptionMessageText"].replace("[MSG]", str(unprecedented_exception)).replace(
                "[EXCEPTION]", str(type(unprecedented_exception).__name__)
            ),
            section["pleaseReinstallText"],
            section["pressEnterText"]
        )))

        while True:
            if readchar.readkey() == readchar.key.ENTER:
                sys.exit()

    except KeyboardInterrupt:
        clear()
        sys.exit()


def unsafe_start():
    # Unsafe start crashes in an exception.
    TheDifferentiationQuiz(configurations, language)  # Starts the program


# Running program
if __name__ == "__main__":
    clear()
    if configurations.program_data["verify_file_presence"]:
        verification_language_section = language.section_get("fileVerification")
        print(verification_language_section["verifyingFilesText"])
        verification = Verifier.verify()
        print()
        if not verification[0]:
            print("\n".join((
                verification_language_section["fileMissingText"],
                verification_language_section["errorDescriptionText"].replace("[FILE]", verification[1])
            )))
            sys.exit()
        else:
            print(verification_language_section["filesVerifiedText"])
            clear()

    if configurations.program_data["safe_start"]:
        safe_start()
    else:
        unsafe_start()

