"""
Term objects have a coefficient and power value attached to themselves.
"""


class Term:
    def __init__(self, coefficient=1.0, power=1.0):
        self.coefficient = coefficient
        self.power = power if coefficient != 0 else 1.0

    def visualize(self):
        """Gets string representation of the Term object. (e.g. 12, 5x, 2x^2, etc)"""
        if self.coefficient == 0:
            return "0"
        elif self.power != 0:
            starting_coefficient_representation = \
                '' if self.coefficient == 1 else '-' if self.coefficient == -1 else self.coefficient
            return f"{starting_coefficient_representation}x{'^' + str(self.power) if self.power != 1 else ''}"
        else:
            return str(self.coefficient)

    def visualize_no_sign(self):
        """visualize() but omits the sign. Also returns the sign() value of the term."""
        if (visualized := self.visualize())[0] == "-":
            return visualized[1:], -1
        else:
            return visualized, 1 if visualized != "0" else 0

    def differentiated(self):
        """Differentiates term using power rule. (d/dx of x^n = nx^(n-1) )."""
        if self.power != 0:
            return Term(coefficient=self.coefficient * self.power, power=self.power - 1)
        return Term(0, 0)  # Empty term (represented as 0)

    def copy(self):
        """Returns Term instance with the same coefficient and power."""
        return Term(coefficient=self.coefficient, power=self.power)

    def _integrated(self):
        """UNUSED @ V1.0.0: Integrates using power rule. (integral of x^n = x^(n+1) / n + 1) [without the + C]"""
        try:
            return Term(coefficient=self.coefficient / (self.power + 1), power=self.power+1)
        except ZeroDivisionError:
            return None  # ln rule or whatever not planned out for now

