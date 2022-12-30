# Imports
import random
from expression import Expression


# Question base
class Question:
    def __init__(self, question_type):
        self.question_type = question_type
        self.involved_expression = Expression()
        self.involved_question = ""
        self.minimum_terms_in_question = 2
        self.power_depth = 2  # Power depth: the higher, the more likely there is a power that is higher than normal
        self.answers = []  # First answer is always correct
        self.involved_order = None  # Only available at type 1 questions

    # Modifications functions (Every modification is a list with 4 elements that are all useful in some way)
    def get_random_coefficient(self, allow_negative=False):
        generation_range = (1 if not allow_negative else -6, 6)
        coefficient = random.randint(*generation_range)
        return coefficient if coefficient != 0 else coefficient + random.choice((-1, 1))

    def get_modifications(self, maximum_modifications_amount=3):  # Creates random modifications
        modifications = []
        if self.question_type == 2:
            differentiated_expression = self.involved_expression.differentiated()  # If the list of answers has bools then a new differentiated form must be made

        # This burner expression will be used to remove randomly selected terms
        burner_expression = self.answers[
            0].pseudocopy() if self.question_type == 1 else differentiated_expression.pseudocopy()

        # This will create randomly selected modifiations. The burner expression is used to alter unaltered terms.
        for modification in range(maximum_modifications_amount):
            if not len(burner_expression.terms):
                break  # If the expression is empty, stop
            term = random.choice(burner_expression.terms)
            modifications.append([
                self.answers[0].terms.index(term) if self.question_type == 1 else differentiated_expression.terms.index(
                    term),  # Index of the term, using the correct answer as the burner is modified every rotation
                random.randint(1, 2),  # 1 - Alter the coefficient, 2 - Alter the power
                random.choice([(random.randint(-3, -1)), random.randint(1, 3)]),  # Amount to increment the coefficient/power,
                term.power  # Residue variable that is only used in some cases
            ])
            burner_expression.terms.remove(term)
        return sorted(modifications, key=lambda x: x[0])

    def apply_modifications(self, modifications, expression):  # Applies modifications to expression
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

    def alter_modifications(self, modifications, previous):  # Changes existing modifications
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
            notation_in_question = f"d{f'^{order}' if order > 1 else ''}{function_name}/dx{f'^{order}' if order > 1 else ''}"
        return f"{notation_in_question} = {expression.visualize()}"

    # Generates question based on its type
    def generate(self, maximum_amount_of_terms, allow_negative_powers, order_limit=1):
        used_powers = list(
            range(0 if not allow_negative_powers else 0 - self.power_depth, maximum_amount_of_terms + self.power_depth))
        # Building the expression
        for term in range(random.randint(self.minimum_terms_in_question, maximum_amount_of_terms)):
            power = random.choice(used_powers)
            self.involved_expression.add_term(
                coefficient=self.get_random_coefficient(allow_negative_powers),
                power=power
            )
            used_powers.remove(power)
        self.involved_expression.sort()
        self.involved_question = self.involved_expression.visualize()

        match self.question_type:
            case 1:  # Question type 1: Find derivative of expression
                # Generating answer based on kind of order
                self.involved_order = random.randint(1, order_limit)
                match self.involved_order:
                    case 1:
                        self.answers.append(self.involved_expression.differentiated())
                    case 2 | 3:
                        if len(self.involved_expression.terms) > self.involved_order - 1:
                            self.answers.append(self.involved_expression.differentiated().differentiated())
                            if self.involved_order == 3:
                                self.answers[0] = self.answers[0].differentiated()
                        else:
                            self.involved_order = 1
                            self.answers.append(self.involved_expression.differentiated())

                # Adding wrong answers as mere copies
                for wrong_answer in range(3):
                    self.answers.append(self.answers[0].copy())

                # Modifying wrong answers (and making them all unique)
                modifications = [self.get_modifications()]
                for wrong_answer_index in range(1, 4):
                    self.apply_modifications(modifications[-1], self.answers[wrong_answer_index])
                    modifications.append(self.alter_modifications(modifications[-1], modifications))
                    self.answers[wrong_answer_index].clean_up()

            case 2:  # Question type 2: Check if given derivative is correct
                # Getting symbols
                function_symbol = chr((random.randint(97, 122)))
                use_lagrange_notation = random.choice((True, False))

                # Getting answer
                self.answers = [True, False][::random.choice((1, -1))]  # sneaky way to randomize this list
                self.involved_question = [function_symbol + " = " + self.involved_expression.visualize()]
                appearing_expression = self.involved_expression.differentiated()

                if self.answers[1]:  # If the answer IS NOT supposed to be correct
                    # Modifying terms
                    self.apply_modifications(self.get_modifications(2), appearing_expression)
                self.involved_question.append(
                    self.visualize_with_notation(function_symbol, appearing_expression, use_lagrange_notation))

            case 3:  # Question type 3: Find correct notation and order of derivative
                # Getting notation for the question and the derivative
                use_lagrange_notation = random.choice((True, False))
                function_symbol = chr(random.choice((random.randint(97, 122), random.randint(65, 90))))
                appearing_expression = self.involved_expression.copy()
                for i in range(order := random.randint(1, self.involved_expression.degree())):
                    appearing_expression = appearing_expression.differentiated()
                self.involved_question = f"{function_symbol}{'(x)' if use_lagrange_notation else ''} = {self.involved_expression.visualize()}"

                # Making correct answer
                orders_available = {str(order): [] for order in list(range(1, self.involved_expression.degree() + 1))}
                # orders_available = list(range(1, self.involved_expression.degree() + 1))
                self.answers = [
                    self.visualize_with_notation(function_symbol, appearing_expression, use_lagrange_notation, order)]
                orders_available[str(order)].append(
                    "lagrange" if use_lagrange_notation else "leibniz")  # Lagrange: f'(x), Leibniz: dy/dx
                # Orders are stored in a dict with a value of 2 lists for every order (to track if 1 notation or 2 have been used)

                # Checking which level polynomial the question is to add any extra orders needed
                if len(self.involved_expression.terms) > len(orders_available):
                    for extra_order in range(self.involved_expression.degree() + 1,
                                             self.involved_expression.degree() + len(
                                                     self.involved_expression.terms) - len(orders_available) + 1):
                        orders_available[str(self.involved_expression.degree() + extra_order + 1)] = []

                # Creation of wrong notations
                for wrong_answer_number in range(3):
                    random_order = random.choice(
                        list({str(key): value for key, value in orders_available.items() if len(value) != 2}.keys()))
                    use_lagrange_notation_in_wrong_answer = random.choice((True, False)) if not orders_available[
                        random_order] else orders_available[random_order][0] == "leibniz"
                    self.answers.append(
                        self.visualize_with_notation(function_symbol, appearing_expression,
                                                     use_lagrange_notation_in_wrong_answer, int(random_order))
                    )
                    orders_available[random_order].append(
                        "lagrange" if use_lagrange_notation_in_wrong_answer else "leibniz")
