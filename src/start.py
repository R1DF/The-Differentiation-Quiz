

if __name__ == "__main__":
    # Imports + starting exception handling (exception handler messages default to English)
    try:
        import colorama
        import sys
        import os
        from config_loader import Configurations
        from lang_loader import LanguagePack
        from main import TheDifferentiationQuiz

        configurations = Configurations(os.path.join("config", "conf.toml"))
        language = LanguagePack(os.path.join("lang", configurations.defaults["language"]))

    except (ModuleNotFoundError, ImportError) as exception:
        print(f"{colorama.Fore.RED}An error occurred while running the program:\n"
              f"{'Could not locate a necessary module to import.' if type(exception).__name__ == 'ModuleNotFoundError' else 'Could not import a class or function.'}\n" 
              f"Exception message: {exception} [{type(exception).__name__}]\n\n"
              f"Please reinstall the game. {colorama.Style.RESET_ALL}\n"
              f"[LANGUAGE DEFAULTED TO ENGLISH]\n")
        sys.exit()

    except Exception as exception:
        print(f"{colorama.Fore.RED}An unusual error occurred while running the program...\n"
              f"Exception message: {exception} [{type(exception).__name__}]\n\n"
              f"Please reinstall the game. {colorama.Style.RESET_ALL}\n"
              f"[LANGUAGE DEFAULTED TO ENGLISH]\n")
        sys.exit()

    differentiation_quiz = TheDifferentiationQuiz()  # Starts the program

