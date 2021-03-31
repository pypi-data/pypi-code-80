"""
MSWHIMScores
~~~

MS-WHIM scores were derived from 36 electrostatic potential properties derived
from the three-dimensional structure of the 20 natural amino acids

Zaliani, A., & Gancia, E. (1999). MS-WHIM scores for amino acids: a new
3D-description for peptide QSAR and QSPR studies. Journal of chemical
information and computer sciences, 39(3), 525-533.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_mswhim_scores_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("MSWHIM")


class MSWHIMScores(DescriptorFeaturizer):

    """

    MS-WHIM scores were derived from 36 electrostatic potential properties derived
    from the three-dimensional structure of the 20 natural amino acids

    References
    ----

    Zaliani, A., & Gancia, E. (1999). MS-WHIM scores for amino acids: a new
    3D-description for peptide QSAR and QSPR studies. Journal of chemical
    information and computer sciences, 39(3), 525-533.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_mswhim_scores_codebook(self._aa_list)
