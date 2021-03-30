import os

from musicscore.musictree.midi import C

from musurgia.unittest import TestCase
from musurgia.fractaltree.fractalmusic import FractalMusic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.fm = FractalMusic(proportions=[1, 2, 3, 4], tree_permutation_order=[3, 1, 4, 2], quarter_duration=20,
                               tempo=70)
        self.fm.midi_generator.midi_range = [36, 60]

    def test_get_multi_chord_midis_bad_number_of_midis(self):
        self.fm.add_layer()
        node = self.fm.get_children()[0]
        with self.assertRaises(ValueError):
            node.get_multi_chord_midis_with_range_factor(number_of_midis=0)

        with self.assertRaises(ValueError):
            node.get_multi_chord_midis_with_range_interval(range_interval=10, number_of_midis=0)

    def test_get_multi_chord_midis_number_of_midis_None(self):
        self.fm.add_layer()
        node = self.fm.get_children()[0]
        actual = len(node.get_multi_chord_midis_with_range_factor())
        expected = len(node.children_generated_midis)
        self.assertEqual(actual, expected)
        actual = len(node.get_multi_chord_midis_with_range_interval(10))
        self.assertEqual(expected, actual)

    def test_get_multi_chord_midis_range_interval(self):
        self.fm.add_layer()
        node = self.fm.get_children()[0]
        multi_chord_midis = node.get_multi_chord_midis_with_range_interval(10)
        actual = abs(multi_chord_midis[-1] - multi_chord_midis[0])
        expected = 10
        self.assertEqual(expected, actual)

    def test_get_multi_chord_midis_range_factor(self):
        self.fm.add_layer()
        node = self.fm.get_children()[0]
        multi_chord_midis = node.get_multi_chord_midis_with_range_factor(3)
        actual = abs(multi_chord_midis[-1] - multi_chord_midis[0])
        original_midi_range = node.midi_generator.midi_range

        expected = abs(original_midi_range[1] - original_midi_range[0]) * 3
        self.assertEqual(expected, actual)

    def test_get_multi_chord_midis_with_range_interval_microtone(self):
        self.fm.add_layer()
        node = self.fm.get_children()[0]
        actual = node.get_multi_chord_midis_with_range_interval(10, microtone=4)
        expected = [44.0, 45.5, 50.5, 50.5, 54.0]
        self.assertEqual(expected, actual)

    def test_get_multi_chord_midis_with_range_factor_microtone(self):
        self.fm.add_layer()
        node = self.fm.get_children()[0]
        actual = node.get_multi_chord_midis_with_range_factor(node.calculate_range_factor(10), microtone=4)
        expected = [44.0, 45.5, 50.5, 50.5, 54.0]
        self.assertEqual(expected, actual)

    def test_get_multi_chord_with_range_factor_microtone(self):
        self.fm.add_layer()
        score = self.fm.get_score(layer_number=1)
        for leaf in self.fm.traverse_leaves():
            multi_chord_midis = leaf.get_multi_chord_midis_with_range_factor(range_factor=1.5, microtone=4,
                                                                             no_duplicates=True)
            leaf.chord.midis = multi_chord_midis
        sf = self.fm.get_simple_format()
        sf.auto_clef()
        sf.to_stream_voice().add_to_score(score, 2)

        xml_path = path + '_get_multi_chord_with_range_factor.xml'
        score.write(path=xml_path)

        self.assertCompareFiles(actual_file_path=xml_path)

    def test_get_multi_chord_with_range_factor_original_direction(self):
        self.fm.midi_generator.microtone = 4
        self.fm.add_layer()
        score = self.fm.get_score(layer_number=1)
        for leaf in self.fm.traverse_leaves():
            multi_chord_midis = leaf.get_multi_chord_midis_with_range_factor(range_factor=1, microtone=4,
                                                                             no_duplicates=True,
                                                                             original_direction=True)
            leaf.chord.midis = multi_chord_midis
        sf = self.fm.get_simple_format()
        sf.auto_clef()
        sf.to_stream_voice().add_to_score(score, 2)

        self.fm.add_layer()
        sf = self.fm.get_simple_format()
        sf.auto_clef()
        sf.to_stream_voice().add_to_score(score, 3)

        xml_path = path + '_get_multi_chord_with_range_factor_original_direction.xml'
        score.write(path=xml_path)

        self.assertCompareFiles(actual_file_path=xml_path)

    def test_get_multi_chord_with_range_interval(self):
        self.fm.add_layer()
        score = self.fm.get_score(layer_number=1)
        for leaf in self.fm.traverse_leaves():
            range_interval = 6 + ((leaf.fractal_order - 1) * 1.5)
            number_of_midis = leaf.fractal_order + 1
            midis = leaf.get_multi_chord_midis_with_range_interval(range_interval=range_interval,
                                                                   microtone=4,
                                                                   number_of_midis=number_of_midis)
            leaf.chord.add_words(number_of_midis)
            leaf.chord.midis = midis
        sf = self.fm.get_simple_format()
        sf.auto_clef()
        sf.to_stream_voice().add_to_score(score, 2)
        xml_path = path + '_get_multi_chord_with_range_interval.xml'
        score.write(path=xml_path)

        self.assertCompareFiles(actual_file_path=xml_path)

    def test_calculate_range_factor_wrong_number_of_chords_1(self):
        self.fm.add_layer()
        with self.assertRaises(ValueError):
            self.fm.get_children()[0].calculate_range_factor(midi_range_interval=0)

    def test_calculate_range_factor_one_node(self):
        self.fm.add_layer()
        actual = self.fm.get_children()[0].calculate_range_factor(midi_range_interval=10)
        expected = 0.8333333333333334
        self.assertEqual(expected, actual)

    def test_calculate_range_factor(self):
        fm = FractalMusic(proportions=(1, 2, 3, 4, 5, 6, 7), tree_permutation_order=(2, 6, 4, 1, 3, 7, 5),
                          quarter_duration=30, tempo=60)
        fm.midi_generator.midi_range = [60, 84]
        multi_chord_midi_range_interval = 11
        fm.add_layer()
        actual = [leaf.calculate_range_factor(multi_chord_midi_range_interval) for leaf in
                  fm.traverse_leaves()]
        expected = [-3.6666666666666665,
                    -1.2222222222222223,
                    -1.8333333333333333,
                    11.0,
                    2.2,
                    1.1,
                    1.375]
        self.assertEqual(expected, actual)
