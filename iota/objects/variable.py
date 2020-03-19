"""

Contains definitions for terminal values in the system.

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


class Variable(Value):
    """
    Representation of a variable (to be evaluated)
    """

    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def eval(self, val_dict=None):
        # Evaluate to value if given in val_dict, otherwise remain
        return val_dict.get(self.name, self) if val_dict is not None else self

    def __str__(self):
        return self.name

    def diff(self, wrt):
        # Derivative is 1 if Variable is subject of differentation, else 0
        return 1 if wrt == self.name else 0

    def __eq__(self, other):
        # Compare variable names
        if isinstance(other, Variable):
            return self.name == other.name
        return False
