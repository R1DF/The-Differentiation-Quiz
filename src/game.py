# Imports
import random
from question import Question
from utils.text import success

# Game class
class Game:
    def __init__(
            self,
            amount_of_questions,
            allowed_question_types: list[int],
            use_negative_powers,
            allowed_skips
    ):
        self.amount_of_questions = amount_of_questions
        self.allowed_question_types = allowed_question_types
        self.has_negative_powers = use_negative_powers
        self.questions = []
        self.correctly_answered = 0
        self.questions_skipped = 0
        self.skips_left = allowed_skips

    def generate(self, maximum_amount_of_terms, track_generation=False, question_number_text=None, success_text = ""):
        question_types = {
            "2": random.randint(1, 4) if 2 in self.allowed_question_types else 0,
            "3": random.randint(1, 4) if 3 in self.allowed_question_types else 0
        }
        question_types["1"] = self.amount_of_questions - question_types["2"] - question_types["3"]
        currently_available_types = [int(x) for x in question_types.keys() if x != 0]

        for question in range(self.amount_of_questions):
            question_type = random.choice(currently_available_types)
            if track_generation:
                print(question_number_text.replace("[N]", str(question + 1)), end=" ")
            self.questions.append(
                Question(question_type)
            )
            self.questions[question].generate(maximum_amount_of_terms, self.has_negative_powers)
            if track_generation:
                success(success_text)

            question_types[str(question_type)] -= 1
            if question_types[str(question_type)] == 0:
                currently_available_types.remove(question_type)

