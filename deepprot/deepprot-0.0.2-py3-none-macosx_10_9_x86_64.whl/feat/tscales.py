"""
TScales
~~~

T-scales are based on 67 common topological descriptors of 135 amino acids.
These topological descriptors are based on the connectivity table of amino
acids alone, and to not explicitly consider 3D properties of each structure.

Tian F, Zhou P, Li Z: T-scale as a novel vector of topological descriptors for
amino acids and its application in QSARs of peptides. J Mol Struct. 2007, 830:
106-115. 10.1016/j.molstruc.2006.07.004.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_tscales_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("tScales")


class TScales(DescriptorFeaturizer):

    """
    T-scales are based on 67 common topological descriptors of 135 amino acids.
    These topological descriptors are based on the connectivity table of amino
    acids alone, and to not explicitly consider 3D properties of each structure.

    References
    ----

    Tian F, Zhou P, Li Z: T-scale as a novel vector of topological descriptors for
    amino acids and its application in QSARs of peptides. J Mol Struct. 2007, 830:
    106-115. 10.1016/j.molstruc.2006.07.004.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_tscales_codebook(self._aa_list)
