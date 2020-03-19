from .value import simplify
from .value import Val, Value
from .value import make_constants

import math
from typing import Dict


class Operator(Value):
    precedence = 0

    @make_constants
    def __init__(self, *vals: Value):
        super().__init__()

        self.vals = vals

    def eval(self, val_dict: Dict = None):
        pass

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
