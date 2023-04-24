from fractions import Fraction

class SimplexNumber:
    def __init__(self, fraction: Fraction, M=0) -> None:
        self.real = Fraction(fraction)
        self.M = M

    def __eq__(self, other):
        return self.real == other.real and self.M == other.M if isinstance(other, SimplexNumber) else False

    def __ne__(self, other):
        return not (self == other) if isinstance(other, SimplexNumber) else False

    def __lt__(self, other):
        if type(other) is Fraction or type(other) is int:
            return self.real + self.M * 1e20 < other
        return (self.M, self.real) < (other.M, other.real)

    def __le__(self, other):
        if type(other) is Fraction or type(other) is int:
            return self.real + self.M * 1e20 <= other
        return (self.M, self.real) <= (other.M, other.real)

    def __gt__(self, other):
        if type(other) is Fraction or type(other) is int:
            return self.real + self.M * 1e20 > other
        return (self.M, self.real) > (other.M, other.real)

    def __ge__(self, other):
        if type(other) is Fraction or type(other) is int:
            return self.real + self.M * 1e20 >= other
        return (self.M, self.real) >= (other.M, other.real)

    def __add__(self, other):
        if type(other) is Fraction or type(other) is int:
            return SimplexNumber(self.real + other, self.M)
        else:
            return SimplexNumber(self.real + other.real, self.M + other.M)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) is Fraction:
            return SimplexNumber(self.real - other, self.M)
        else:
            return SimplexNumber(self.real - other.real, self.M - other.M)

    def __mul__(self, other):
        if type(other) is Fraction or type(other) is float:
            return SimplexNumber(self.real * other, self.M * other)
        return SimplexNumber(self.real * other.real, self.real * other.M + other.real * self.M)

    def __truediv__(self, other):
        if type(other) is SimplexNumber:
            return SimplexNumber(self.real / other.real, self.M)
        return SimplexNumber(self.real / other, self.M)

    def __neg__(self):
        return SimplexNumber(-self.real, -self.M)

    def __str__(self) -> str:
        real = self.real if self.real != 0 else ''
        M_coefficient = str(abs(self.M)) if abs(self.M) != 1 else '' 
        M = f'{M_coefficient}M' if self.M != 0 else ''
        sign = ('+' if self.M > 0 else '-') if M != '' else ''

        return f'{real}{sign}{M}' if (real or M) else '0'

    def __repr__(self) -> str:
        return str(self)