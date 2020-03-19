import unittest

from .. import Variable


class TestVariable(unittest.TestCase):
    """ Test the Variable Class"""

    def test_init(self):
        x = Variable('x')

    def test_self_diff(self):
        x = Variable('x')
        self.assertEqual(x.diff('x'), 1)

    def test_self_other(self):
        x = Variable('x')
        self.assertEqual(x.diff('y'), 0)

    def test_eval(self):
        x = Variable('x')
        self.assertEqual(x.eval({'x': 8}), 8)
