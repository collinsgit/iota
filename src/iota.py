"""
This module contains all definitions of various components of the system.
"""

import math
from typing import Dict, Union


""" Terminal components of the language that are operated on. """

# Representation of a numerical value.
Val = Union[float, int]


# TODO: make this much more intelligent
def make_constants(f):
    def with_constants(*args, **kwargs):
        args = map(lambda x: x if isinstance(x, Value) else Constant(x), args)

        return f(*args, **kwargs)
    return with_constants


def simplify(f):
    def wrapper(*args, **kwargs):
        output = f(*args, **kwargs)

        return output.eval() if isinstance(output, Value) else output
    return wrapper


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

    @simplify
    def diff(self, wrt):
        raise NotImplementedError


class Variable(Value):
    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def eval(self, val_dict=None):
        return val_dict.get(self.name, self) if val_dict is not None else self

    def __str__(self):
        return self.name

    def diff(self, wrt):
        return 1 if wrt == self.name else 0


class Constant(Value):
    def __init__(self, val: Val):
        super().__init__()

        self.val = val

    def eval(self, val_dict=None):
        return self.val

    def __str__(self):
        return str(self.val)

    def diff(self, wrt):
        return 0

    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.val == other.val
        elif isinstance(other, Val.__args__):
            return self.val == other
        return False


class Operator(Value):
    precedence = 0

    @make_constants
    def __init__(self, *vals: Value):
        super().__init__()

        self.vals = vals

    def diff(self, wrt):
        raise NotImplementedError


def parenthesize(val: Value, paren_type: type = Operator, precedence: float = 0.):
    val_str = str(val)
    val_precedence = val.precedence if isinstance(val, Operator) else 0

    if val_precedence < precedence and isinstance(val, paren_type):
        if val_str[0] != '(' or val_str[-1] != ')':
            val_str = '(' + val_str + ')'
    return val_str


class BinaryOperator(Operator):
    symbol = ''

    def __init__(self, *vals: Value):
        super().__init__(*vals)

        assert len(vals) == 2

    def __str__(self):
        sub_strings = []

        for i, val in enumerate(self.vals):
            sub_string = parenthesize(val, precedence=self.precedence + (0.1 if i else 0.))

            sub_strings.append(sub_string)

        # TODO: consider that spacing is not needed for all operators (i.e. powers)
        return (' ' + self.symbol + ' ').join(sub_strings)

    def diff(self, wrt):
        raise NotImplementedError


class Sum(BinaryOperator):
    symbol = '+'

    def eval(self, val_dict=None):
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        if l_val == 0.:
            return r_val
        elif r_val == 0.:
            return l_val

        return r_val + l_val

    @simplify
    def diff(self, wrt):
        return self.vals[0].diff(wrt) + self.vals[1].diff(wrt)


class Difference(BinaryOperator):
    symbol = '-'

    def eval(self, val_dict=None):
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        if l_val == 0.:
            return -r_val
        elif r_val == 0.:
            return l_val

        return l_val - r_val

    @simplify
    def diff(self, wrt):
        return self.vals[0].diff(wrt) - self.vals[1].diff(wrt)


class Product(BinaryOperator):
    precedence = 1
    symbol = '*'

    def eval(self, val_dict=None):
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        if l_val == 0. or r_val == 0.:
            return 0.
        elif l_val == 1.:
            return r_val
        elif r_val == 1.:
            return l_val

        return l_val * r_val

    @simplify
    def diff(self, wrt):
        return self.vals[0] * self.vals[1].diff(wrt) + self.vals[0].diff(wrt) * self.vals[1]


class Division(BinaryOperator):
    precedence = 1
    symbol = '/'

    def eval(self, val_dict=None):
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        if l_val == 0.:
            return 0.
        elif r_val == 0.:
            raise ZeroDivisionError
        elif r_val == 1.:
            return l_val

        return l_val / r_val

    @simplify
    def diff(self, wrt):
        return (self.vals[1] * self.vals[0].diff(wrt) - self.vals[0] * self.vals[1].diff(wrt)) / (self.vals[1] * self.vals[1])


class Power(Operator):
    precedence = 2
    symbol = '^'

    def eval(self, val_dict=None):
        base = self.vals[0].eval(val_dict)
        power = self.vals[1].eval(val_dict)

        if power == 0.:
            return 1
        elif power == 1.:
            return base
        elif base == 0. or base == 1.:
            return base

        return base ** power

    def __str__(self):
        base_str = parenthesize(self.vals[0], precedence=self.precedence)
        power_str = parenthesize(self.vals[1], precedence=self.precedence)

        return base_str + self.symbol + power_str

    @simplify
    def diff(self, wrt):
        return self.vals[1] * self.vals[0].diff(wrt) * self.vals[0] ** (self.vals[1] - 1)


class Logarithm(Operator):
    precedence = 2

    def __str__(self):
        if len(self.vals) == 1:
            antilog = str(self.vals[0])

            return 'ln({})'.format(antilog)
        elif len(self.vals) == 2:
            base = str(self.vals[0])
            antilog = str(self.vals[1])

            return 'log({}, {})'.format(base, antilog)
        else:
            raise NotImplementedError

    def eval(self, val_dict=None):
        if len(self.vals) == 1:
            base = math.e
            antilog = self.vals[0].eval(val_dict)
        else:
            base = self.vals[0].eval(val_dict)
            antilog = self.vals[1].eval(val_dict)

        if isinstance(base, Val.__args__):
            if antilog == 1.:
                return 0.
            elif antilog == base:
                return 1.

            if isinstance(antilog, Val.__args__):
                return math.log(antilog, base)
            else:
                return Logarithm(antilog) if base == math.e else Logarithm(base, antilog)
        else:
            raise NotImplementedError

    @simplify
    def diff(self, wrt):
        if len(self.vals) == 1:
            base = math.e
            antilog = self.vals[0]
        else:
            base = self.vals[0].eval()
            antilog = self.vals[1]

        if isinstance(base, Val.__args__):
            return antilog.diff(wrt) / (math.log(base) * antilog)
        else:
            raise NotImplementedError


if __name__ == '__main__':
    exp = Logarithm(5 + ((Constant(1.) * Constant(3.) - Variable('x')) / Constant(4.) + 4) ** 5)

    print(exp)
    print(exp.eval())
    print(exp.diff('x'))
