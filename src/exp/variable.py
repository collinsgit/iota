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
    def __sub__(self, other):
        return Difference(self, other)

    @make_constants
    def __mul__(self, other):
        return Product(self, other)

    @make_constants
    def __truediv__(self, other):
        return Division(self, other)

    @make_constants
    def __pow__(self, power, modulo=None):
        return Power(self, power)


class Variable(Value):
    def __init__(self, name: str = None):
        super().__init__()

        self.name = name

    def eval(self, val_dict=None):
        return val_dict.get(self.name, self) if val_dict is not None else self


class Constant(Value):
    def __init__(self, val: Val):
        super().__init__()

        self.val = val

    def eval(self, val_dict=None):
        return self.val


class Operator(Value):
    def __init__(self, *vals: Value):
        super().__init__()

        self.vals = vals

    def eval(self, val_dict=None):
        pass


class Sum(Operator):
    def eval(self, val_dict=None):
        return sum(map(lambda x: x.eval(val_dict), self.vals))


class Difference(Operator):
    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) - self.vals[1].eval(val_dict)


class Product(Operator):
    def eval(self, val_dict=None):
        return reduce(operator.mul, map(lambda x: x.eval(val_dict), self.vals))


class Division(Operator):
    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) / self.vals[1].eval(val_dict)


class Power(Operator):
    def eval(self, val_dict=None):
        return self.vals[0].eval(val_dict) ** self.vals[1].eval(val_dict)


if __name__ == '__main__':
    exp = (Constant(1.) * Constant(3.) + Constant(5.)) / Constant(4.) + 4

    print(exp.eval())
