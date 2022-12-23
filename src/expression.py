# Imports
from term import Term


# Expression base
class Expression:
    def __init__(self, terms: list[Term] = None):
        self.terms = terms if terms is not None else []  # Using mutable default arguments is a blunder

    def degree(self):
        return max(self.terms, key=lambda term: term.power).power   # Returns the degree of the polynomial (e.g. x^2 is highest power -> 2)

    def add_term(self, coefficient, power):
        """Adds a term object."""
        self.terms.append(Term(coefficient=coefficient, power=power if coefficient != 0 else 1))

    def get_sorted(self, visualized=False):
        """Returns a copied list of the terms but sorted based on the power of x in each term. (ascending order)"""
        terms = sorted(self.terms, key=lambda term: term.power)[::-1]  # Sorts by powers (x^2 > x > 1 > x^-1)
        return terms if not visualized else [x.visualize() for x in terms]

    def sort(self):
        """self.get_sorted(), but changes self.terms to the result."""
        self.terms = self.get_sorted()

    def visualize(self):
        """Prints out the string representation of the terms for readable output by the user."""
        visualized = ""
        for term in self.get_sorted():
            if term.coefficient != 0:
                visualized += f"{'- ' if term.coefficient < 0 else '+ '}{term.visualize_no_sign()[0]} "
        return visualized[0 if visualized[0] == "-" else 2:-1]

    def clean_up(self):
        """Removes all terms that are equal to 0. Returns self as an updated list if it needs to be saved."""
        self.terms = [x for x in self.terms if x.coefficient != 0]
        return self

    def differentiated(self):
        """Returns an Expression() object which has all the terms differentiated."""
        return Expression([x.differentiated() for x in self.terms]).clean_up()  # Cleaned up to remove any zeroes

    def copy(self):
        """Returns another Expression instance with the same terms"""
        return Expression([x.copy() for x in self.terms])  # Returns copy of itself

    def pseudocopy(self):
        """copy() but the Terms inside are the same as the original term. Do not use unless you know what you're doing."""
        return Expression([x for x in self.terms])

    # def same(self, other_expression):
    #     """Checks if the expression contains the exact same terms with the given one."""
    #     self_terms_copied = self.get_sorted()
    #     other_terms_sorted = other_expression.get_sorted()
    #
    #     if len(self_terms_copied) != len(other_terms_sorted):
    #         return False
    #
    #     for term_index, term in enumerate(self_terms_copied):
    #         other_term = other_terms_sorted[term_index]
    #         if term.coefficient != other_term.coefficient or term.power != other_term.power:
    #             return False
    #
    #     return True
