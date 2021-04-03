import unittest

from numformat import autoformat


class TestAutoFormatWithMaxStrLength(unittest.TestCase):

    def test_invalid_max_str_length(self):
        with self.assertRaises(ValueError):
            autoformat(10.0, max_sig_figs=2, max_length=1)

    def test_zeros(self):
        self.assertEqual('0.0', autoformat(0.0, max_sig_figs=2, max_length=3))
        self.assertEqual('0.0', autoformat(0.000, max_sig_figs=2, max_length=3))
        self.assertEqual('0.0', autoformat(0.000, max_sig_figs=4, max_length=4))
        self.assertEqual('0.000', autoformat('0.000', max_sig_figs=2, max_length=5))
        self.assertEqual('0.000', autoformat('0.000', max_sig_figs=4, max_length=4))

    def test_integers(self):
        # Positive integers
        self.assertEqual('1', autoformat(1, max_sig_figs=2, max_length=3))
        self.assertEqual('2', autoformat(2, max_sig_figs=2, max_length=3))
        self.assertEqual('13', autoformat(13, max_sig_figs=3, max_length=3))
        self.assertEqual('1000', autoformat(1000, max_sig_figs=2, max_length=3))
        self.assertEqual('4.59e+08', autoformat(459284756, max_sig_figs=18, max_length=8))

        # Negative integers
        self.assertEqual('-1', autoformat(-1, max_sig_figs=2, max_length=3))
        self.assertEqual('-2', autoformat(-2, max_sig_figs=2, max_length=3))
        self.assertEqual('-13', autoformat(-13, max_sig_figs=3, max_length=3))
        self.assertEqual('-1000', autoformat(-1000, max_sig_figs=2, max_length=3))
        self.assertEqual('-4.6e+08', autoformat(-459284756, max_sig_figs=18, max_length=8))

    def test_floats(self):
        # Positive floats
        self.assertEqual('0.0032', autoformat(0.0032, max_sig_figs=3, max_length=6))
        self.assertEqual('3e-3', autoformat(0.0032, max_sig_figs=3, max_length=5))
        self.assertEqual('145.89', autoformat(145.89, max_sig_figs=6, max_length=6))
        self.assertEqual('1.3e+06', autoformat(1300001.0, max_sig_figs=10, max_length=7))
        self.assertEqual('12700', autoformat(12700.00, max_sig_figs=4, max_length=6))
        self.assertEqual('12700.0', autoformat(12700.00, max_sig_figs=8, max_length=8))

        # Negative floats
        self.assertEqual('-0.0032', autoformat(-0.0032, max_sig_figs=3, max_length=7))
        self.assertEqual('-145.89', autoformat(-145.89, max_sig_figs=6, max_length=7))
        self.assertEqual('-1.3e+06', autoformat(-1300001.0, max_sig_figs=10, max_length=8))
        self.assertEqual('-12700', autoformat(-12700.00, max_sig_figs=4, max_length=6))
        self.assertEqual('-12700.0', autoformat(-12700.00, max_sig_figs=8, max_length=8))

    def test_strings_max_sig_figs_greater_than_actual_sig_figs(self):
        # Positive integers
        self.assertEqual('1', autoformat('1', max_sig_figs=2, max_length=3))
        self.assertEqual('2', autoformat('2', max_sig_figs=2, max_length=3))
        self.assertEqual('13', autoformat('13', max_sig_figs=3, max_length=3))
        self.assertEqual('1000', autoformat('1000', max_sig_figs=2, max_length=3))
        self.assertEqual('4.59e+08', autoformat('459284756', max_sig_figs=18, max_length=8))

        # Negative integers
        self.assertEqual('-1', autoformat('-1', max_sig_figs=2, max_length=3))
        self.assertEqual('-2', autoformat('-2', max_sig_figs=2, max_length=3))
        self.assertEqual('-13', autoformat('-13', max_sig_figs=3, max_length=3))
        self.assertEqual('-1000', autoformat('-1000', max_sig_figs=2, max_length=3))
        self.assertEqual('-4.6e+08', autoformat('-459284756', max_sig_figs=18, max_length=8))

        # Positive floats
        self.assertEqual('0.0032', autoformat('0.0032', max_sig_figs=3, max_length=6))
        self.assertEqual('3e-3', autoformat('0.0032', max_sig_figs=3, max_length=5))
        self.assertEqual('145.89', autoformat('145.89', max_sig_figs=6, max_length=6))
        self.assertEqual('1.3e+06', autoformat('1300001.0', max_sig_figs=10, max_length=7))
        self.assertEqual('12700', autoformat('12700.00', max_sig_figs=4, max_length=6))
        self.assertEqual('12700.00', autoformat('12700.00', max_sig_figs=8, max_length=8))

        # Negative floats
        self.assertEqual('-0.0032', autoformat('-0.0032', max_sig_figs=3, max_length=7))
        self.assertEqual('-145.89', autoformat('-145.89', max_sig_figs=6, max_length=7))
        self.assertEqual('-1.3e+06', autoformat('-1300001.0', max_sig_figs=10, max_length=8))
        self.assertEqual('-12700', autoformat('-12700.00', max_sig_figs=4, max_length=6))
        self.assertEqual('-1.27e+04', autoformat('-12700.000', max_sig_figs=8, max_length=9))
        self.assertEqual('-12700.00', autoformat('-12700.00', max_sig_figs=8, max_length=9))
