# Imports
import random
from expression import Expression

# Question base
class Question:
    def __init__(self, question_type):
        self.question_type = question_type
        self.involved_expression = Expression()
        self.involved_question = ""
        self.answers = []  # First answer is always correct

    # Modifications functions (Every modification is a list with 4 elements that are all useful in some way)
    def get_modifications(self, maximum_modifications_amount=3):
        modifications = []
        burner_expression = self.answers[0].pseudocopy()
        for modification in range(maximum_modifications_amount):
            if not len(burner_expression.terms):
                break
            term = random.choice(burner_expression.terms)
            modifications.append([
                self.answers[0].terms.index(term),  # Index of the term, using the correct answer as the burner is modified every rotation
                random.randint(1, 2),  # 1 - Coefficient, 2 - Power
                random.choice([(random.randint(-3, -1)), random.randint(1, 3)]),  # Modifier,
                term.power
            ])
            burner_expression.terms.remove(term)
        return sorted(modifications, key=lambda x: x[0])

    def apply_modifications(self, modifications, expression):
        for modifier_value_1, modifier_value_2, modifier_value_3, residue in modifications:
            """
            The values of a modification are ambiguous and that is why the names of the values in the for loop are so vague.
            if modifier_value_1 is "c", then a term with the coefficient of modifier_value_2 and power of modifier_value_3 is made
            if modifier_value_1 is a number, then the term with the index of that number will have either its coefficient of power changed by modifier_value_3
            "residue" is useless here
            """
            if modifier_value_1 == "c":
                expression.add_term(modifier_value_2, modifier_value_3)
            elif modifier_value_2 == 1:
                expression.terms[modifier_value_1].coefficient += modifier_value_3
            else:
                expression.terms[modifier_value_1].power += modifier_value_3

    def alter_modifications(self, modifications, previous):
        new_modifications = modifications.copy()
        skips = 0
        for modification in new_modifications:
            if random.randint(1, 50) <= 15:
                # Refuses to modify specific modification
                if skips < len(modifications) - 2:
                    continue

                # Modifications which add another term do not get modified
                if modification[0] == "c":
                    continue

            modification[2] += random.choice((random.randint(-3, -1), random.randint(1, 3)))

        if new_modifications in previous:
            # If the new modification is not unique, it will create a whole new term (of a unique power)
            used_powers = list({x[3] for x in modifications if x[3] is not None})
            available_powers = list(range(min(used_powers) - 10, max(used_powers) + 10))

            for used_power in used_powers:
                available_powers.remove(used_power)

            new_modifications.append([
                "c",
                random.choice((random.randint(-10, -1), random.randint(1, 10))),  # 1 - Coefficient, 2 - Power
                random.choice(available_powers),
                None
            ])
        return new_modifications

    # Specific visualization function
    def visualize_with_notation(self, function_name, expression, use_lagrange_notation=True, order=1):
        if use_lagrange_notation:
            single_quote_character = "\'"
            notation_in_question = f"{function_name}{order * single_quote_character if order <= 3 else f'({order})'}(x)"
        else:
            notation_in_question = f"d{function_name}{f'^{order}' if order > 1 else ''}/dx{f'^{order}' if order > 1 else ''}"
        return f"{notation_in_question} = {expression.visualize()}"

    # Generates question based on its type
    def generate(self, minimum_amount_of_terms, allow_negative_powers, allow_decimal_powers):
        used_powers = list(range(minimum_amount_of_terms - 5, minimum_amount_of_terms + 5))
        # Building the expression

        for term in range(random.randint(2, minimum_amount_of_terms)):
            power = random.choice(used_powers)
            self.involved_expression.add_term(coefficient=random.randint(1, 6) * random.choice((1, 1, -1 if allow_negative_powers else 1)), power=power)
            used_powers.remove(power)
        self.involved_expression.sort()
        self.involved_question = self.involved_expression.visualize()

        match self.question_type:
            case 1:  # Question type 1: Find derivative of expression
                # Getting answer
                self.answers.append(self.involved_expression.differentiated())

                # Adding wrong answers as mere copies
                for wrong_answer in range(3):
                    self.answers.append(self.answers[0].copy())

                # Modifying wrong answers (and making them all unique)
                modifications = [self.get_modifications()]
                for wrong_answer_index in range(3):
                    self.apply_modifications(modifications[-1], self.answers[wrong_answer_index + 1])
                    modifications.append(self.alter_modifications(modifications[-1], modifications))

            case 2:   # Question type 2: Check if given derivative is correct
                # Getting answer
                self.answers = [True, False][::random.choice((1, -1))]  # sneaky way to randomize this list
                appearing_expression = self.involved_expression.differentiated()

                if self.answers[1]:  # If the answer IS NOT supposed to be correct
                    # Modifying terms
                    self.apply_modifications(self.get_modifications(2), appearing_expression)
                self.involved_question = appearing_expression.visualize()

            case 3:   # Question type 3: Find correct notation and order of derivative
                # Getting notation for the question and the derivative
                use_lagrange_notation = random.choice((True, False))
                function_symbol = chr(random.choice((random.randint(97, 122), random.randint(65, 90))))
                appearing_expression = self.involved_expression.copy()
                for i in range(order := random.randint(1, self.involved_expression.degree())):
                    appearing_expression = appearing_expression.differentiated()
                self.involved_question = f"{function_symbol}{'(x)' if use_lagrange_notation else ''} = {self.involved_expression.visualize()}"

                # Making correct answer
                orders_available = list(range(1, self.involved_expression.degree() + 1))
                self.answers = [self.visualize_with_notation(function_symbol, appearing_expression, use_lagrange_notation, order)]
                orders_available.remove(order)

                for wrong_answer_number in range(3):
                    random_order = random.choice(orders_available)
                    self.answers.append(
                        self.visualize_with_notation(function_symbol, appearing_expression, use_lagrange_notation if random.randint(1, 80) <= 70 else not use_lagrange_notation, random_order)
                    )
                    orders_available.remove(random_order)

