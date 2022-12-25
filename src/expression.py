# Imports
from term import Term


# Expression base
class Expression:
    def __init__(self, terms: list[Term] = None):
        self.terms = terms if terms is not None else []  # Using mutable default arguments is a blunder

    def degree(self):
        """Returns the power of x of the term with the highest (absolute) value for x (when exponentiated)."""
        return max(self.terms, key=lambda term: term.power).power   # Returns the degree of the polynomial (e.g. x^2 is highest power -> 2)

    def lowest_power(self):
        """Returns the term with the lowest power of x in the expression."""
        return min(self.terms, key=lambda term: term.power).power

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
        if self.terms:
            for term in self.get_sorted():
                if term.coefficient != 0:
                    visualized += f"{'- ' if term.coefficient < 0 else '+ '}{term.visualize_no_sign()[0]} "
            return visualized[0 if visualized[0] == "-" else 2:-1]
        else:
            return "0"

    def clean_up(self):
        """Removes all terms that are equal to 0 and combines like terms. Returns self as an updated list if it needs to be saved."""
        self.terms = [x for x in self.terms if x.coefficient != 0]
        powers = [term.power for term in self.terms]
        for power in set(powers):
            if powers.count(power) > 1:
                like_terms = [term for term in self.terms if term.power == power]
                combined_coefficients_sum = sum((term.coefficient for term in like_terms))
                for term in like_terms:
                    self.terms.remove(term)
                self.terms.append(Term(coefficient=combined_coefficients_sum, power=power))
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

