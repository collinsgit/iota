"""

Representation of ranges of functions/distributions

"""

from .value import Val


class Range:
    """
    A general range, which must have contains checking and iteration
    """

    def __init__(self):
        pass

    def __contains__(self, item: Val):
        # Must be implemented in children
        raise NotImplementedError

    def __iter__(self):
        # Must be implemented in children
        raise NotImplementedError


class ContinuousRange:
    """
    A continuous range over an interval [a,b]
    """

    def __init__(self, a: Val, b: Val, closed=True):
        self.a = a
        self.b = b
        self.closed = closed

        # Must be proper, non-zero interval
        assert a < b

    def __contains__(self, item: Val):
        # Check that item is between bounds
        return self.a < item < self.b

    def __iter__(self, step=0.1):
        x = self.a

        # Iterate over interval according to step size
        while x <= self.b:
            yield x
            x += step


class DiscreteRange:
    """
    A discrete range over a set {a,b,c,...}
    """

    def __init__(self, elems: set):
        self.elems = elems

    def __contains__(self, item:Val):
        # Check elem set
        return item in self.elems

    def __iter__(self):
        # Iterate over elems
        for x in self.elems:
            yield x


class CompoundRange:
    """
    A range which is a combination of other ranges
    Does not check for repetition
    """

    def __init__(self, ranges: set):
        self.ranges = ranges

    def __contains__(self, item):
        # Check if item in any sub-range
        for sub_range in self.ranges:
            if item in sub_range:
                return True
        return False

    def __iter__(self):
        # Yield from sub-ranges
        for sub_range in self.ranges:
            yield from sub_range
