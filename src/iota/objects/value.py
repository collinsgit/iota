from typing import Dict, Union


""" Terminal components of the language that are operated on. """

# Representation of a numerical value.
Val = Union[float, int]


def simplify(f):
    def wrapper(*args, **kwargs):
        output = f(*args, **kwargs)

        return output.eval() if isinstance(output, Value) else output
    return wrapper


class Value:
    def __init__(self):
        pass

    def __str__(self):
        return ''

    def eval(self, val_dict: Dict = None):
        pass

    @simplify
    def diff(self, wrt):
        raise NotImplementedError
