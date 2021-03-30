from musurgia.fractaltree.midigenerators import RelativeMidi
from musurgia.unittest import TestCase


class TestRelativeMidis(TestCase):
    def test_midi_range(self):
        midi_range = [44, 54]
        proportions = [2, 4, 1, 3]
        directions = [-1, -1, 1, 1]
        midi_generator = RelativeMidi(midi_range=midi_range, proportions=proportions, directions=directions)
        actual = sorted(list(midi_generator.iterator))
        expected = [44.0, 46.0, 51.0, 51.0, 54.0]
        self.assertEqual(expected, actual)
