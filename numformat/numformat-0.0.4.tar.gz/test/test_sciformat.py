import unittest

from numformat import sciformat


class TestSciFormat(unittest.TestCase):

    def test_zeros(self):
        self.assertEqual('0e+00', sciformat(0))
        self.assertEqual('0e-1', sciformat(0.0))
        self.assertEqual('0e-1', sciformat(0.000))
        self.assertEqual('0e-3', sciformat('0.000'))

    def test_integers(self):
        # Positive integers
        self.assertEqual('1e+00', sciformat(1))
        self.assertEqual('2e+00', sciformat(2))
        self.assertEqual('1.3e+01', sciformat(13))
        self.assertEqual('1e+03', sciformat(1000))
        self.assertEqual('4.59284756e+08', sciformat(459284756))

        # Negative integers
        self.assertEqual('-1e+00', sciformat(-1))
        self.assertEqual('-2e+00', sciformat(-2))
        self.assertEqual('-1.3e+01', sciformat(-13))
        self.assertEqual('-1e+03', sciformat(-1000))
        self.assertEqual('-4.59284756e+08', sciformat(-459284756))

    def test_floats(self):
        # Positive floats
        self.assertEqual('3.2e-3', sciformat(0.0032))
        self.assertEqual('1.4589e+2', sciformat(145.89))
        self.assertEqual('1.3000010e+6', sciformat(1300001.0))
        self.assertEqual('1.27000e+4', sciformat(12700.00))

        # Negative floats
        self.assertEqual('-3.2e-3', sciformat(-0.0032))
        self.assertEqual('-1.4589e+2', sciformat(-145.89))
        self.assertEqual('-1.3000010e+6', sciformat(-1300001.0))
        self.assertEqual('-1.27000e+4', sciformat(-12700.00))

    def test_strings(self):
        # Positive integers
        self.assertEqual('1e+00', sciformat('1'))
        self.assertEqual('2e+00', sciformat('2'))
        self.assertEqual('1.3e+01', sciformat('13'))
        self.assertEqual('1e+03', sciformat('1000'))
        self.assertEqual('4.59284756e+08', sciformat('459284756'))

        # Negative integers
        self.assertEqual('-1e+00', sciformat('-1'))
        self.assertEqual('-2e+00', sciformat('-2'))
        self.assertEqual('-1.3e+01', sciformat('-13'))
        self.assertEqual('-1e+03', sciformat('-1000'))
        self.assertEqual('-4.59284756e+08', sciformat('-459284756'))

        # Positive floats
        self.assertEqual('3.2e-3', sciformat('0.0032'))
        self.assertEqual('1.4589e+2', sciformat('145.89'))
        self.assertEqual('1.3000010e+6', sciformat('1300001.0'))
        self.assertEqual('1.270000e+4', sciformat('12700.00'))

        # Negative floats
        self.assertEqual('-3.2e-3', sciformat('-0.0032'))
        self.assertEqual('-1.4589e+2', sciformat('-145.89'))
        self.assertEqual('-1.3000010e+6', sciformat('-1300001.0'))
        self.assertEqual('-1.270000e+4', sciformat('-12700.00'))
