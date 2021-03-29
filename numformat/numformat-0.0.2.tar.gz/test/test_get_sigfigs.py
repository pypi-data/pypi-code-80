import unittest

from numformat.operators.operator_factory import OperatorFactory


class TestGetSigFigs(unittest.TestCase):

    def test_zeros(self):
        self.assertEqual(0, self._get_sigfigs(0))
        self.assertEqual(0, self._get_sigfigs(0.0))
        self.assertEqual(0, self._get_sigfigs(0.000))

    def test_positive_int(self):
        self.assertEqual(1, self._get_sigfigs(1))
        self.assertEqual(1, self._get_sigfigs(2))
        self.assertEqual(2, self._get_sigfigs(13))
        self.assertEqual(1, self._get_sigfigs(1000))
        self.assertEqual(9, self._get_sigfigs(459284756))

    def test_negative_int(self):
        self.assertEqual(1, self._get_sigfigs(-1))
        self.assertEqual(1, self._get_sigfigs(-2))
        self.assertEqual(2, self._get_sigfigs(-13))
        self.assertEqual(1, self._get_sigfigs(-1000))
        self.assertEqual(9, self._get_sigfigs(-459284756))

    def test_positive_float(self):
        self.assertEqual(4, self._get_sigfigs(27.36))
        self.assertEqual(2, self._get_sigfigs(0.0032))
        self.assertEqual(5, self._get_sigfigs(1270.000))
        self.assertEqual(7, self._get_sigfigs(12000.01))

    def test_negative_float(self):
        self.assertEqual(4, self._get_sigfigs(-27.36))
        self.assertEqual(2, self._get_sigfigs(-0.0032))
        self.assertEqual(5, self._get_sigfigs(-1270.000))
        self.assertEqual(7, self._get_sigfigs(-12000.01))

    def test_string(self):
        self.assertEqual(0, self._get_sigfigs('0'))
        self.assertEqual(0, self._get_sigfigs('0.0'))
        self.assertEqual(0, self._get_sigfigs('0.000'))
        self.assertEqual(1, self._get_sigfigs('1'))
        self.assertEqual(1, self._get_sigfigs('2'))
        self.assertEqual(2, self._get_sigfigs('13'))
        self.assertEqual(1, self._get_sigfigs('1000'))
        self.assertEqual(9, self._get_sigfigs('459284756'))
        self.assertEqual(1, self._get_sigfigs('-1'))
        self.assertEqual(1, self._get_sigfigs('-2'))
        self.assertEqual(2, self._get_sigfigs('-13'))
        self.assertEqual(1, self._get_sigfigs('-1000'))
        self.assertEqual(9, self._get_sigfigs('-459284756'))
        self.assertEqual(4, self._get_sigfigs('27.36'))
        self.assertEqual(2, self._get_sigfigs('0.0032'))
        self.assertEqual(7, self._get_sigfigs('1270.000'))
        self.assertEqual(7, self._get_sigfigs('12000.01'))
        self.assertEqual(4, self._get_sigfigs('-27.36'))
        self.assertEqual(2, self._get_sigfigs('-0.0032'))
        self.assertEqual(7, self._get_sigfigs('-1270.000'))
        self.assertEqual(7, self._get_sigfigs('-12000.01'))

    def _get_sigfigs(self, value):
        operator = OperatorFactory.get_operator(value)
        return operator.get_sigfigs()
