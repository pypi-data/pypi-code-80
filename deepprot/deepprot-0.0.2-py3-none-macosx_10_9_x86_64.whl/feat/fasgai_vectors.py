"""
FASGAIVectors
~~~

The FASGAI vectors (Factor Analysis Scales of Generalized Amino Acid
Information) is a set of amino acid descriptors, that reflects hydrophobicity,
alpha and turn propensities, bulky properties, compositional characteristics,
local flexibility, and electronic properties, that can be utilized to represent
the sequence structural features of peptides or protein motifs.

Liang, G., & Li, Z. (2007). Factor analysis scale of generalized amino acid
information as the source of a new set of descriptors for elucidating the
structure and activity relationships of cationic antimicrobial peptides.
Molecular Informatics, 26(6), 754-763.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_fasgai_vector_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("FASGAI")


class FASGAIVectors(DescriptorFeaturizer):

    """
    The FASGAI vectors (Factor Analysis Scales of Generalized Amino Acid
    Information) is a set of amino acid descriptors, that reflects hydrophobicity,
    alpha and turn propensities, bulky properties, compositional characteristics,
    local flexibility, and electronic properties, that can be utilized to represent
    the sequence structural features of peptides or protein motifs.

    References
    ----

    Liang, G., & Li, Z. (2007). Factor analysis scale of generalized amino acid
    information as the source of a new set of descriptors for elucidating the
    structure and activity relationships of cationic antimicrobial peptides.
    Molecular Informatics, 26(6), 754-763.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_fasgai_vector_codebook(self._aa_list)
