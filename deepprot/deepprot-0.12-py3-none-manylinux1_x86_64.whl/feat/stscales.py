"""
STScales
~~~

ST-scales were proposed by Yang et al, taking 827 properties into account which
are mainly constitutional, topological, geometrical, hydrophobic, elec- tronic,
and steric properties of a total set of 167 AAs.

Yang, L., Shu, M., Ma, K., Mei, H., Jiang, Y., & Li, Z. (2010). ST-scale as a
novel amino acid descriptor and its application in QSAM of peptides and
analogues. Amino acids, 38(3), 805-816.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_stscales_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("stScales")


class STScales(DescriptorFeaturizer):

    """

    ST-scales were proposed by Yang et al, taking 827 properties into account which
    are mainly constitutional, topological, geometrical, hydrophobic, elec- tronic,
    and steric properties of a total set of 167 AAs.

    References
    ----

    Yang, L., Shu, M., Ma, K., Mei, H., Jiang, Y., & Li, Z. (2010). ST-scale as a
    novel amino acid descriptor and its application in QSAM of peptides and
    analogues. Amino acids, 38(3), 805-816.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_stscales_codebook(self._aa_list)
