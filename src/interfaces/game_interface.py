# Imports
import questionary
from .base import InterfaceCL
from utils.text import get_language_entry, get_utility_entry, break_line
from utils.system import clear, wait_for_enter
from game import Game
from random import shuffle
from specific_exception import GameException


# Game loader interface
class GameInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name, game: Game):
        self.game = game
        super().__init__(master, language_section_name)

    def scramble_answers(self, answers):
        scrambled = answers.copy()
        correct_answer = scrambled[0]
        shuffle(scrambled)
        return scrambled, scrambled.index(correct_answer)

    def load_interface(self):
        self.yes_text, self.no_text = get_utility_entry(self.master, "closedQuestionAnswers")
        for question_index, question in enumerate(self.game.questions):
            clear()
            # Printing question number
            print(get_language_entry(self, "questionNumberText").replace("[N]", str(question_index + 1)))

            # Getting question header text and the answers
            involved_question = question.involved_question
            match question.question_type:
                case 1:
                    header = get_language_entry(self, f"{['first', 'second', 'third'][question.involved_order - 1]}OrderDerivativeQuestionText")
                    answers, correct_answer_index = self.scramble_answers([x.visualize() for x in question.answers])
                case 2:
                    header = get_language_entry(self, "isCorrectQuestionText")
                    answers = list(map(lambda x: self.yes_text if x else self.no_text, question.answers))
                    correct_answer_index = answers.index(self.yes_text)
                case 3:
                    header = get_language_entry(self, "notationQuestionText")
                    answers, correct_answer_index = self.scramble_answers(question.answers)
                case _:
                    raise GameException("invalid question type")

            print(header)
            print(involved_question if isinstance(involved_question, str) else "\n".join(involved_question))
            break_line()

            # Printing out formatted answers and getting user selection
            shown_answers = [chr(65 + x) for x in range(len(answers))]
            if self.game.skips_left:
                shown_answers.append(get_language_entry(self, "skipChoiceText"))

            for answer, letter in zip(answers, shown_answers):
                print(f"{letter}. {answer}")
            break_line()

            user_answer = shown_answers.index(questionary.select(
                get_language_entry(self, "answerQueryText"),
                choices=shown_answers
            ).unsafe_ask())

            if user_answer == len(answers):  # If skipped
                print("skip")
            elif user_answer == correct_answer_index:  # If correctly answered
                print("correct")
            else:  # If question answered wrongly
                print("idiot")

            wait_for_enter(self.master.language_pack)