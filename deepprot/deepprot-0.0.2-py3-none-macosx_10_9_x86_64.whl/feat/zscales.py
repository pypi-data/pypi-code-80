"""
zScales
~~~

Z-scales are based on physicochemical properties of the AAs including NMR data
and thin-layer chromatography (TLC) data.

Sandberg M, Eriksson L, Jonsson J, Sjostrom M, Wold S: New chemical descriptors
relevant for the design of biologically active peptides. A multivariate
characterization of 87 amino acids. J Med Chem 1998, 41:2481-2491.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_zscales_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("zScales")


class ZScales(DescriptorFeaturizer):

    """Converts a string of amino acids to Z-scale vector representation.

    Z-scales are based on physicochemical properties of the AAs including NMR data
    and thin-layer chromatography (TLC) data.

    References
    ----
    Sandberg M, Eriksson L, Jonsson J, Sjostrom M, Wold S: New chemical descriptors
    relevant for the design of biologically active peptides. A multivariate
    characterization of 87 amino acids. J Med Chem 1998, 41:2481-2491.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_zscales_codebook(self._aa_list)
