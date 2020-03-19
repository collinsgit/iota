"""

Top-level definition of all components in the system.

"""

from typing import Dict, Union

# Representation of a numerical value.
Val = Union[float, int]


# TODO: make this much more intelligent
def make_constants(f):
    def with_constants(*args, **kwargs):
        # Everything that isn't a Value is assumed to be an outside number
        # It is then converted to a Constant
        args = map(lambda x: x if isinstance(x, Value) else Constant(x), args)

        return f(*args, **kwargs)
    return with_constants


def simplify(f):
    # Reduce expression to simplest form
    def wrapper(*args, **kwargs):
        output = f(*args, **kwargs)

        # Evaluate expression to combine adjacent constants
        return output.eval() if isinstance(output, Value) else output
    return wrapper


class Value:
    """
    Base representation of an object which composed expressions.
    May be an operator or an element being operated on.
    """

    def __init__(self):
        pass

    def eval(self, val_dict: Dict = None):
        # Evaluation is null initially
        pass

    # all arithmetic dunders point to BinaryOperations
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
        # Differentiation of a value with respect to variable named by wrt
        raise NotImplementedError


# It is important to import Operator in the highest level component in order to
# override built-in operators on iota's definitions. However, this introduces a
# circular dependency as Operator is a subclass of Value. In order to prevent
# Python from breaking, we must include this import at the bottom of the file
# so that the namespace of Value is already defined by the time the below line
# is reached.
from .operator import *  # noqa: E402
