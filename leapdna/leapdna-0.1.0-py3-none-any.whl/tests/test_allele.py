from leapdna.blocks.locus import Locus
from .support import TestCase
from leapdna.blocks import Allele


class TestAllele(TestCase):
    def test_can_be_instantiated(self):
        l = Locus('l1')
        a = Allele('a1', l)

        self.assertIn('llele', str(a))