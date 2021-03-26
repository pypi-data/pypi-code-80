import unittest

from .. import dezanza

class DezanzaTests(unittest.TestCase):

    def test_empty_seq(self):
        """Dezanza with empty string.
        """

        with self.assertRaises(ValueError):
            dezanza([])

    def test_invalid_format(self):
        """Dezanza with invalid input format.
        """

        with self.assertRaises(ValueError):
            dezanza([102, 3, 4, 5])

    def test_ok(self):
        """Dezanza with valid input.
        """

        res = dezanza([[102], 9, 0, -13, -1, 17])
        expected = "foobar"
        self.assertEqual(res, expected)
