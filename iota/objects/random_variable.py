"""

General definition of a random variable

"""

from .value import Value
from .variable import Variable
from .range import Range


class RandomVariable(Variable):
    """
    Representation of Random Variable
    """

    def __init__(self, name, density: Value, range: Range):
        super().__init__(name)

        self.density = density
        self.range = range

    def sample(self):
        # Sampling must be implemented
        raise NotImplementedError

    def expect(self):
        # Expectation must be implemented (maybe this should change)
        raise NotImplementedError
