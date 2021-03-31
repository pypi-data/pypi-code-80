"""
vhseScales
~~~

VHSE-scales (principal components score Vectors of Hydrophobic, Steric, and
Electronic properties), are derived from principal components analysis (PCA) on
independent families of 18 hydrophobic properties, 17 steric properties, and 15
electronic properties, respectively, which are included in total 50
physicochemical variables of 20 coded amino acids.

Mei, H. U., Liao, Z. H., Zhou, Y., & Li, S. Z. (2005). A new set of amino acid
descriptors and its application in peptide QSARs. Peptide Science, 80(6),
775-786.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_vhse_scales_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("VHSE")


class VHSEScales(DescriptorFeaturizer):

    """Converts a string of amino acids to Z-scale vector representation.

    VHSE-scales (principal components score Vectors of Hydrophobic, Steric, and
    Electronic properties), are derived from principal components analysis (PCA) on
    independent families of 18 hydrophobic properties, 17 steric properties, and 15
    electronic properties, respectively, which are included in total 50
    physicochemical variables of 20 coded amino acids.

    References
    ----

    Mei, H. U., Liao, Z. H., Zhou, Y., & Li, S. Z. (2005). A new set of amino acid
    descriptors and its application in peptide QSARs. Peptide Science, 80(6),
    775-786.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_vhse_scales_codebook(self._aa_list)
