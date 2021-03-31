"""
CrucianiProperties
~~~

This function calculates the Cruciani properties of an amino-acids sequence
using the scaled principal component scores that summarize a broad set of
descriptors calculated based on the interaction of each amino acid residue with
several chemical groups (or "probes"), such as charged ions, methyl, hydroxyl
groups, and so forth.

Cruciani, G., Baroni, M., Carosati, E., Clementi, M., Valigi, R., and Clementi,
S. (2004) Peptide studies by means of principal properties of amino acids
derived from MIF descriptors. J. Chemom. 18, 146-155.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_cruciani_properties_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("crucianiProperties")


class CrucianiProperties(DescriptorFeaturizer):

    """Converts a string of amino acids to Cruciani property vectors.

    VHSE-scales (principal components score Vectors of Hydrophobic, Steric, and
    Electronic properties), are derived from principal components analysis (PCA) on
    independent families of 18 hydrophobic properties, 17 steric properties, and 15
    electronic properties, respectively, which are included in total 50
    physicochemical variables of 20 coded amino acids.

    References
    ----

    Cruciani, G., Baroni, M., Carosati, E., Clementi, M., Valigi, R., and Clementi,
    S. (2004) Peptide studies by means of principal properties of amino acids
    derived from MIF descriptors. J. Chemom. 18, 146-155.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_cruciani_properties_codebook(self._aa_list)
