import json
import unittest

from .. import zanza

class ZanzaTests(unittest.TestCase):

    def test_empty_string(self):
        """Zanza with empty string.
        """

        with self.assertRaises(ValueError):
            zanza("")

    def test_ok(self):
        """Zanza with valid input.
        """

        res = zanza("foobarbaz")
        expected = [[1, 0, 2], 9, 0, -13, -1, 17, -16, -1, 25]
        self.assertEqual(res, expected)
