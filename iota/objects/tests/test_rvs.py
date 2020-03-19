import unittest

from .. import Uniform


class TestUniform(unittest.TestCase):
    """ Test the Uniform Random Variable """

    def test_init(self):
        x = Uniform('x', 1, 2)

    def test_sample(self):
        x = Uniform('x', -1, 0)
        sample = x.sample()
        self.assertGreaterEqual(sample, -1)
        self.assertLessEqual(sample, 0)

    def test_expect(self):
        x = Uniform('x', 10, 20)
        expect = x.expect()
        self.assertEqual(expect, 15.)
