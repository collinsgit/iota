from .value import Val, Value


# TODO: make this much more intelligent
def make_constants(f):
    def with_constants(*args, **kwargs):
        args = map(lambda x: x if isinstance(x, Value) else Constant(x), args)

        return f(*args, **kwargs)
    return with_constants


class Constant(Value):
    def __init__(self, val: Val):
        super().__init__()

        self.val = val

    def eval(self, val_dict=None):
        return self.val

    def __str__(self):
        return str(self.val)

    def diff(self, wrt):
        return 0

    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.val == other.val
        elif isinstance(other, Val.__args__):
            return self.val == other
        return False


class Variable(Value):
    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def eval(self, val_dict=None):
        return val_dict.get(self.name, self) if val_dict is not None else self

    def __str__(self):
        return self.name

    def diff(self, wrt):
        return 1 if wrt == self.name else 0
