import unittest

from .. import Constant


class TestConstant(unittest.TestCase):
    """ Test the Constant Class"""

    def test_int(self):
        c = Constant(5)

    def test_float(self):
        c = Constant(-1.1)

    def test_diff(self):
        c = Constant(1)
        self.assertEqual(c.diff('x'), 0)
