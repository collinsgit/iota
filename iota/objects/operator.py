"""

Relations between different values are defined below through operators.

"""

from .value import simplify
from .value import Val, Value
from .value import make_constants

import math
from typing import Dict


class Operator(Value):
    """
    Represents operators, or values which act on other values
    """

    precedence = 0

    @make_constants
    def __init__(self, *vals: Value):
        super().__init__()

        # Values being acted upon
        self.vals = vals

    def eval(self, val_dict: Dict = None):
        # Evaluation remains null
        pass

    def diff(self, wrt):
        # Differentiation remains unimplemented
        raise NotImplementedError


def parenthesize(val: Value, paren_type: type = Operator, precedence: float = 0.):
    """
    Function to wrap parentheses around Value string
    :param val:
    :param paren_type:
    :param precedence:
    :return: A string representing the expression, in parenthesized form
    """
    val_str = str(val)
    val_precedence = val.precedence if isinstance(val, Operator) else 0

    # Check that precedence difference necessitates parentheses
    if val_precedence < precedence and isinstance(val, paren_type):
        # Check to ensure parentheses are not redundant
        if val_str[0] != '(' or val_str[-1] != ')':
            val_str = '(' + val_str + ')'
    return val_str


class BinaryOperator(Operator):
    """
    Represents all operators which take in two values
    """

    symbol = ''

    def __init__(self, *vals: Value):
        super().__init__(*vals)

        # Assert that operation is binary
        assert len(vals) == 2

    def __str__(self):
        sub_strings = []

        for i, val in enumerate(self.vals):
            # Parenthesize components if lower precedence
            sub_string = parenthesize(val, precedence=self.precedence + (0.1 if i else 0.))

            sub_strings.append(sub_string)

        # TODO: consider that spacing is not needed for all operators (i.e. powers)
        return (' ' + self.symbol + ' ').join(sub_strings)

    def diff(self, wrt):
        raise NotImplementedError


class Sum(BinaryOperator):
    """
    Represent summation of values
    """

    symbol = '+'

    def eval(self, val_dict=None):
        # Evaluate left and right, then add
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        # Ignore 0 values
        if l_val == 0.:
            return r_val
        elif r_val == 0.:
            return l_val

        return r_val + l_val

    @simplify
    def diff(self, wrt):
        # Apply linearity of differentation
        return self.vals[0].diff(wrt) + self.vals[1].diff(wrt)


class Difference(BinaryOperator):
    """
    Represent difference between values
    """

    symbol = '-'

    def eval(self, val_dict=None):
        # Evaluate left and right, then subtract
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        # Ignore 0 values
        if l_val == 0.:
            return -r_val
        elif r_val == 0.:
            return l_val

        return l_val - r_val

    @simplify
    def diff(self, wrt):
        # Apply linearity of differentation
        return self.vals[0].diff(wrt) - self.vals[1].diff(wrt)


class Product(BinaryOperator):
    """
    Represent product of values
    """

    precedence = 1
    symbol = '*'

    def eval(self, val_dict=None):
        # Evaluate left and right, then multiply
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        # Simplify in null/identity cases
        if l_val == 0. or r_val == 0.:
            return 0.
        elif l_val == 1.:
            return r_val
        elif r_val == 1.:
            return l_val

        return l_val * r_val

    @simplify
    def diff(self, wrt):
        # Apply product rule
        return self.vals[0] * self.vals[1].diff(wrt) + self.vals[0].diff(wrt) * self.vals[1]


class Division(BinaryOperator):
    """
    Represent division of values
    """

    precedence = 1
    symbol = '/'

    def eval(self, val_dict=None):
        # Evaluate left and right, then divide
        l_val = self.vals[0].eval(val_dict)
        r_val = self.vals[1].eval(val_dict)

        # Simplify in null/identity cases
        if l_val == 0.:
            return 0.
        elif r_val == 0.:
            raise ZeroDivisionError
        elif r_val == 1.:
            return l_val

        return l_val / r_val

    @simplify
    def diff(self, wrt):
        # Apply quotient rule
        return (self.vals[1] * self.vals[0].diff(wrt) - self.vals[0] * self.vals[1].diff(wrt)) / (self.vals[1] * self.vals[1])


class Power(Operator):
    """
    Represent exponentiation
    """

    precedence = 2
    symbol = '^'

    def eval(self, val_dict=None):
        # Evaluate base and power, then exponentiate
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
        # Parenthesize base and power, then combine
        base_str = parenthesize(self.vals[0], precedence=self.precedence)
        power_str = parenthesize(self.vals[1], precedence=self.precedence)

        return base_str + self.symbol + power_str

    @simplify
    def diff(self, wrt):
        # y = f(x)^g(x)
        # y' = y * (g'(x) * ln(f(x)) + g(x) * f'(x) / f(x))
        base = self.vals[0]
        power = self.vals[1]

        return self * (power.diff(wrt) * Logarithm(base) + power * base.diff(wrt) / base)


# The definition of some of these simple operators requires some of our extra
# operators. In particular, the derivative of a power relies on the natural
# logarithm. In order to maintain organization of operations, the extra operators
# are in the ops.py file rather than this file, despite the resulting circular
# dependency. The reasoning parallels that given in value.py.
from .ops import *  # noqa: E402
