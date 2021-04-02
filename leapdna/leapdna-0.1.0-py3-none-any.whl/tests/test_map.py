from unittest.case import TestCase
from .support import TestCase

from leapdna.map import get_map, decrease_band_precission, band2coords


class TestMap(TestCase):
    def test_map_loading(self):
        map = get_map()

        self.assertEqual(map['1p36.33'], ('1', 1, 2300000))
        self.assertEqual(map['1p36.3'], ('1', 1, 7100000))

    def test_decrease_band_precission(self):
        seq = '3p12.31a, 3p12.31, 3p12.3, 3p12, 3p1, 3p, 3'.split(', ')
        for i, band in enumerate(seq[:-1]):
            self.assertEqual(decrease_band_precission(band), seq[i + 1])

    def test_band2coords(self):
        self.assertEqual(band2coords('1p36.33abc'), ('1', 1, 2300000))