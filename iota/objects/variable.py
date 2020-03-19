"""

Contains definitions for terminal variable values in the system.

"""


from .value import Value


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
        # Derivative is 1 if Variable is subject of differentiation, else 0
        return 1 if wrt == self.name else 0

    def __eq__(self, other):
        # Compare variable names
        if isinstance(other, Variable):
            return self.name == other.name
        return False
