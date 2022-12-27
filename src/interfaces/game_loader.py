# Imports
from .base import InterfaceCL
from utils.text import get_language_entry, get_alienated_entry, get_utility_entry, break_line
from utils.system import clear, wait_for_enter
from game import Game


# Game loader interface
class GameLoadingInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name, difficulty):
        self.difficulty = difficulty
        super().__init__(master, language_section_name)

    def load_interface(self):
        clear()
        difficulty_name = get_alienated_entry(self.master, "gameSetup", "difficultiesQueryChoices")[self.difficulty - 1]
        questions_to_generate = 7 + ((self.difficulty - 1) * 3)   # This formula works great
        maximum_amount_of_terms = self.difficulty + 3  # This one too
        allowed_question_types = [[1], [1, 2], [1, 2, 3]][self.difficulty - 1]
        allowed_skips = [questions_to_generate, 3, 0][self.difficulty - 1]

        print(get_language_entry(self, "selectedDifficultyText").replace("[DIFFICULTY]", difficulty_name))
        break_line()

        print(get_language_entry(self, "generatingQuestionsText").replace("[AMOUNT]", str(questions_to_generate)))
        game = Game(questions_to_generate, allowed_question_types, bool(self.difficulty), allowed_skips)  # Clever loophole abuse on the third argument
        game.generate(maximum_amount_of_terms, True, get_language_entry(self, "generatingQuestionText"), get_utility_entry(self.master, "success"))
        print(get_language_entry(self, "generationCompleteText"))
        break_line()

        wait_for_enter(self.master.language_pack)
        self.master.make_game_interface(game)

