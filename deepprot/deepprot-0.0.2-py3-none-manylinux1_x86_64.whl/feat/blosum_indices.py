"""
BLOSUMIndices
~~~

BLOSUM indices were derived of physicochemical properties that have been
subjected to a VARIMAX analyses and an alignment matrix of the 20 natural AAs
using the BLOSUM62 matrix.

Georgiev, A. G. (2009). Interpretable numerical descriptors of amino acid
space. Journal of Computational Biology, 16(5), 703-723.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_blosum_indices_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("BLOSUM")


class BLOSUMIndices(DescriptorFeaturizer):

    """
    BLOSUM indices were derived of physicochemical properties that have been
    subjected to a VARIMAX analyses and an alignment matrix of the 20 natural AAs
    using the BLOSUM62 matrix.

    References
    ----

    Georgiev, A. G. (2009). Interpretable numerical descriptors of amino acid
    space. Journal of Computational Biology, 16(5), 703-723.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_blosum_indices_codebook(self._aa_list)
