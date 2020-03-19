"""

A variety of additional functions are provided below as operators.

"""


from .operator import Operator
from .value import simplify
from .value import Val


import math


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
