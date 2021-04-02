import unittest
from unittest.case import TestCase
from .support import TestCase

from leapdna.blocks import Locus
from leapdna.map import band2coords, get_map


class TestLocus(TestCase):
    def test_explicit_coords(self):
        l = Locus('L1', coords=('1', 23, 34))
        self.assertEqual(l.get_coords(), ('1', 23, 34))

        l2 = Locus('L2')
        self.assertTrue(l2.get_coords() is None)

    def test_coords_from_band(self):
        map = get_map()
        band = next(iter(map))
        l = Locus('L1', band=band)
        self.assertEqual(l.get_coords(), band2coords(band))
        self.assertTrue(l.get_coords(guess=False) is None)
