import unittest

from numformat import enggformat


class TestEnggFormat(unittest.TestCase):

    def test_zeros(self):
        self.assertEqual('0', enggformat(0))
        self.assertEqual('0', enggformat(0.0))
        self.assertEqual('0', enggformat(0.000))
        self.assertEqual('0', enggformat('0.000'))

    def test_integers(self):
        # Positive integers
        self.assertEqual('1', enggformat(1))
        self.assertEqual('2', enggformat(2))
        self.assertEqual('13', enggformat(13))
        self.assertEqual('1E+3', enggformat(1000))
        self.assertEqual('459284756', enggformat(459284756))

        # Negative integers
        self.assertEqual('-1', enggformat(-1))
        self.assertEqual('-2', enggformat(-2))
        self.assertEqual('-13', enggformat(-13))
        self.assertEqual('-1E+3', enggformat(-1000))
        self.assertEqual('-459284756', enggformat(-459284756))

    def test_floats(self):
        # Positive floats
        self.assertEqual('0.0032', enggformat(0.0032))
        self.assertEqual('145.89', enggformat(145.89))
        self.assertEqual('1300001', enggformat(1300001.0))
        self.assertEqual('12.7E+3', enggformat(12700.00))

        # Negative floats
        self.assertEqual('-0.0032', enggformat(-0.0032))
        self.assertEqual('-145.89', enggformat(-145.89))
        self.assertEqual('-1300001', enggformat(-1300001.0))
        self.assertEqual('-12.7E+3', enggformat(-12700.00))

    def test_strings(self):
        # Positive integers
        self.assertEqual('1', enggformat('1'))
        self.assertEqual('2', enggformat('2'))
        self.assertEqual('13', enggformat('13'))
        self.assertEqual('1E+3', enggformat('1000'))
        self.assertEqual('459284756', enggformat('459284756'))

        # Negative integers
        self.assertEqual('-1', enggformat('-1'))
        self.assertEqual('-2', enggformat('-2'))
        self.assertEqual('-13', enggformat('-13'))
        self.assertEqual('-1E+3', enggformat('-1000'))
        self.assertEqual('-459284756', enggformat('-459284756'))

        # Positive floats
        self.assertEqual('0.0032', enggformat('0.0032'))
        self.assertEqual('145.89', enggformat('145.89'))
        self.assertEqual('1300001', enggformat('1300001.0'))
        self.assertEqual('12.7E+3', enggformat('12700.00'))

        # Negative floats
        self.assertEqual('-0.0032', enggformat('-0.0032'))
        self.assertEqual('-145.89', enggformat('-145.89'))
        self.assertEqual('-1300001', enggformat('-1300001.0'))
        self.assertEqual('-12.7E+3', enggformat('-12700.00'))
