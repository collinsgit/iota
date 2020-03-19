import unittest

from .. import Constant, Variable


class TestVal(unittest.TestCase):
    """ TODO: Add real tests and get rid of this testing class """

    def test_test(self):
        self.assertTrue(True)


class TestConstant(unittest.TestCase):
    """ Test the Constant Class"""

    def test_int(self):
        c = Constant(5)

    def test_float(self):
        c = Constant(-1.1)

    def test_diff(self):
        c = Constant(1)
        self.assertEqual(c.diff('x'), 0)


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
