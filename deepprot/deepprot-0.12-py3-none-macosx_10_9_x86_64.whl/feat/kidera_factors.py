"""
KideraFactors
~~~

The Kidera Factors were originally derived by applying multivariate analysis to
188 physical properties of the 20 amino acids and using dimension reduction
techniques. This function calculates the average of the ten Kidera factors for
a protein sequence.

Kidera, A., Konishi, Y., Oka, M., Ooi, T., & Scheraga, H. A. (1985).
Statistical analysis of the physical properties of the 20 naturally occurring
amino acids. Journal of Protein Chemistry, 4(1), 23-55.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_kidera_factors_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("kideraFactors")


class KideraFactors(DescriptorFeaturizer):

    """Converts a string of amino acids to Cruciani property vectors.

    VHSE-scales (principal components score Vectors of Hydrophobic, Steric, and
    Electronic properties), are derived from principal components analysis (PCA) on
    independent families of 18 hydrophobic properties, 17 steric properties, and 15
    electronic properties, respectively, which are included in total 50
    physicochemical variables of 20 coded amino acids.

    References
    ----

    Kidera, A., Konishi, Y., Oka, M., Ooi, T., & Scheraga, H. A. (1985).
    Statistical analysis of the physical properties of the 20 naturally occurring
    amino acids. Journal of Protein Chemistry, 4(1), 23-55.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_kidera_factors_codebook(self._aa_list)
