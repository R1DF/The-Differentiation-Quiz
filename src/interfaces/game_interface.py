# Imports
import questionary
from .base import InterfaceCL
from utils.text import get_language_entry, get_utility_entry, break_line, success, warn, alarm
from utils.system import clear, wait_for_enter
from game import Game
from random import shuffle
from specific_exception import GameException


# Game interface
class GameInterfaceCL(InterfaceCL):
    def __init__(self, master, language_section_name, game: Game):
        self.game = game
        self.correct_questions = []
        self.incorrect_questions = []
        self.skipped_questions = []
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
                    header = get_language_entry(self,
                                                f"{['first', 'second', 'third'][question.involved_order - 1]}OrderDerivativeQuestionText")
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
                self.game.questions_skipped += 1
                self.game.skips_left -= 1
                self.skipped_questions.append(question_index + 1)
                print(get_language_entry(self, "skippedText"))
            elif user_answer == correct_answer_index:  # If correctly answered
                self.game.correctly_answered += 1
                self.correct_questions.append(question_index + 1)
                print(get_language_entry(self, "correctAnswerText"))
            else:  # If question answered wrongly
                self.incorrect_questions.append(question_index + 1)
                self.game.incorrectly_answered += 1
                print(get_language_entry(self, "incorrectAnswerText"))

            wait_for_enter(self.master.language_pack)
            clear()
        self.give_results()

    def give_results(self):
        amount_of_questions = len(self.game.questions)
        correct_questions_amount = len(self.correct_questions)
        print(get_language_entry(self, "resultsText"))
        break_line()

        for question_index in range(amount_of_questions):
            print(get_language_entry(self, "questionResultText").replace("[N]", str(question_index + 1)), end=" ")
            if question_index + 1 in self.correct_questions:
                success(get_language_entry(self, "resultTextEntries")[0])
            elif question_index + 1 in self.incorrect_questions:
                alarm(get_language_entry(self, "resultTextEntries")[1])
            else:
                warn(get_language_entry(self, "resultTextEntries")[2])
        break_line()

        try:
            percentage = correct_questions_amount / (amount_of_questions - len(self.skipped_questions))
        except ZeroDivisionError:  # If all questions were skipped
            percentage = 0

        print(get_language_entry(self, "resultFractionText").replace(
            "[CORRECT]", str(correct_questions_amount)).replace(
                "[AMOUNT]", str(amount_of_questions))
        )
        print(get_language_entry(self, "resultPercentageText").replace("[N]", str(round(percentage, 2) * 100)))
        break_line()

        wait_for_enter(self.master.language_pack, True)
        self.master.make_main_menu()

