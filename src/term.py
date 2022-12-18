"""
Term objects have a coefficient and power value attached to themselves.
"""
class Term:
    def __init__(self, coefficient=1.0, power=1.0):
        self.coefficient = coefficient
        self.power = power

    def visualize(self):
        """Gets string representation of the Term object. (e.g. 12, 5x, 2x^2, etc)"""
        if self.coefficient == 0:
            return "0"
        elif self.power != 0:
            return f"{'' if self.coefficient == 1 else self.coefficient}x{'^' + str(self.power) if self.power != 1 else ''}"
        else:
            return str(self.coefficient)

    def differentiated(self):
        """Differentiates term using power rule. (d/dx of x^n = nx^(n-1) )"""
        if self.power != 0:
            return Term(coefficient=self.coefficient * self.power, power=self.power-1)
        else:
            return Term(0, 0)  # Empty term (represented as 0)

    def integrated(self):
        """UNUSED V1.0.0: Integrates using power rule. (integral of x^n = x^(n+1) / n + 1)"""
        try:
            return Term(coefficient=self.coefficient / (self.power + 1), power=self.power+1)
        except ZeroDivisionError:
            return None  # ln rule or whatever not planned out for now
