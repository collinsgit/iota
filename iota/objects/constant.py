"""

Contains definitions for terminal constant values in the system.

"""


from .value import Val, Value


class Constant(Value):
    """
    Representation of a constant (integer or floating point)
    """

    def __init__(self, val: Val):
        super().__init__()

        self.val = val

    def eval(self, val_dict=None):
        # Evaluates to self
        return self.val

    def __str__(self):
        return str(self.val)

    def diff(self, wrt):
        # Constant always has derivative of 0
        return 0

    def __eq__(self, other):
        # If both Constant, compare vals; otherwise, compare self.val to other
        if isinstance(other, Constant):
            return self.val == other.val
        elif isinstance(other, Val.__args__):
            return self.val == other
        return False