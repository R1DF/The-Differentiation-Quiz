# Imports
from term import Term

# Expression base
class Expression:
    def __init__(self, terms=None):
        self.terms = terms if terms is not None else []  # Using mutable default arguments is a blunder

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
        """Removes all terms that are equal to 0."""
        self.terms = [x for x in self.terms if x.coefficient != 0]

    def differentiated(self):
        """Returns an Expression() object which has all the terms differentiated."""
        new_expression = Expression()
        new_expression.terms = [x.differentiated() for x in self.terms]
        new_expression.clean_up()  # Remove any zeroes
        return new_expression

