"""

A collection of various useful random variable types

"""

from .constant import Constant
from .random_variable import RandomVariable
from .range import ContinuousRange, DiscreteRange
from .value import Val

import random


class Uniform(RandomVariable):
    def __init__(self, name, a: Val, b: Val):
        density = Constant(1. / (b - a))
        range = ContinuousRange(a, b)
        super().__init__(name, density, range)

        self.a = a
        self.b = b

    def sample(self):
        # Utilize the random package uniform distribution
        return random.uniform(self.a, self.b)

    def expect(self):
        return (self.a + self.b) / 2


if __name__ == '__main__':
    x = Uniform('x', 1, 2)
    print(x.sample())
    print(x.expect())
