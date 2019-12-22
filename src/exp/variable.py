from functools import reduce
import operator
from typing import Dict, Union


Val = Union[float, int]


# TODO: make this much more intelligent
def make_constants(f):
    def with_constants(*args, **kwargs):
        args = map(lambda x: x if isinstance(x, Value) else Constant(x), args)

        return f(*args, **kwargs)
    return with_constants


class Value:
    def __init__(self):
        pass

    def eval(self, val_dict: Dict = None):
        pass

    @make_constants
    def __add__(self, other):
        return Sum(self, other)

    @make_constants
    def __radd__(self, other):
        return Sum(other, self)

    @make_constants
    def __sub__(self, other):
        return Difference(self, other)

    @make_constants
    def __rsub__(self, other):
        return Difference(other, self)

    @make_constants
    def __mul__(self, other):
        return Product(self, other)

    @make_constants
    def __rmul__(self, other):
        return Product(other, self)

    @make_constants
    def __truediv__(self, other):
        return Division(self, other)

    @make_constants
    def __rtruediv__(self, other):
        return Division(other, self)

    @make_constants
    def __pow__(self, power, modulo=None):
        return Power(self, power)

    def __str__(self):
        return ''


class Variable(Value):
    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def eval(self, val_dict=None):
        return val_dict.get(self.name, self) if val_dict is not None else self

    def __str__(self):
        return self.name


class Constant(Value):
    def __init__(self, val: Val):
        super().__init__()

        self.val = val

    def eval(self, val_dict=None):
        return self.val

    def __str__(self):
        return str(self.val)


class Operator(Value):
    precedence = 0

    def __init__(self, *vals: Value):
        super().__init__()

        self.vals = vals


def parenthesize(val: Value, paren_type: type = Operator, precedence: int = 0):
    val_str = str(val)
    val_precedence = val.precedence if isinstance(val, Operator) else 0

    if val_precedence < precedence and isinstance(val, paren_type):
        val_str = '(' + val_str + ')'
    return val_str


class BinaryOperator(Operator):
    symbol = ''

    def __init__(self, *vals: Value):
        super().__init__(*vals)

        assert len(vals) == 2

    def __str__(self):
        sub_strings = []

        for val in self.vals:
            sub_string = parenthesize(val, precedence=self.precedence)

            sub_strings.append(sub_string)

        # TODO: consider that spacing is not needed for all operators (i.e. powers)
        return (' ' + self.symbol + ' ').join(sub_strings)


class Sum(BinaryOperator):
    symbol = '+'

    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) + self.vals[1].eval(val_dict)


class Difference(BinaryOperator):
    symbol = '-'

    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) - self.vals[1].eval(val_dict)


class Product(BinaryOperator):
    precedence = 1
    symbol = '*'

    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) * self.vals[1].eval(val_dict)


class Division(BinaryOperator):
    precedence = 1
    symbol = '/'

    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) / self.vals[1].eval(val_dict)


class Power(Operator):
    precedence = 2
    symbol = '^'

    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) ** self.vals[1].eval(val_dict)

    def __str__(self):
        base_str = parenthesize(self.vals[0], precedence=self.precedence)
        power_str = parenthesize(self.vals[1], precedence=self.precedence)

        return base_str + self.symbol + power_str


if __name__ == '__main__':
    exp = 5 + ((Constant(1.) * Constant(3.) - Variable('x')) / Constant(4.) + 4) ** 5

    print(exp)
    print(exp.eval())
    print(exp.eval({'x': 1}))
