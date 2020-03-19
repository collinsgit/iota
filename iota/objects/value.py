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


from .operator import *
