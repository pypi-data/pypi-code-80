from leapdna.errors import LeapdnaError
from leapdna.blocks.locus import Locus
from leapdna.blocks.allele import Allele
from .support import TestCase

from leapdna.blocks import Observation


class TestObservationBlock(TestCase):
    def test_can_be_instantiated(self):
        l1 = Locus('l1')
        a1 = Allele('a1', l1)
        obs = Observation(a1, count=2, frequency=0.25)

        self.assertTrue(obs is not None)
        self.assertTrue('bservation' in str(obs))