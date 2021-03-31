"""
ProtFP
~~~

The ProtFP descriptor set was constructed from a large initial selection of
indices obtained from the AAindex database for all 20 naturally occurring amino
acids.

van Westen, G. J., Swier, R. F., Wegner, J. K., IJzerman, A. P., van Vlijmen,
H. W., & Bender, A. (2013). Benchmarking of protein descriptor sets in
proteochemometric modeling (part 1): comparative study of 13 amino acid
descriptor sets. Journal of cheminformatics, 5(1), 41.
"""

from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer
from deepprot.feat.utils import descriptor_from_rdata


def _generate_protfp_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    return descriptor_from_rdata("ProtFP")


class ProtFP(DescriptorFeaturizer):

    """
    The ProtFP descriptor set was constructed from a large initial selection of
    indices obtained from the AAindex database for all 20 naturally occurring amino
    acids.

    References
    ----

    van Westen, G. J., Swier, R. F., Wegner, J. K., IJzerman, A. P., van Vlijmen,
    H. W., & Bender, A. (2013). Benchmarking of protein descriptor sets in
    proteochemometric modeling (part 1): comparative study of 13 amino acid
    descriptor sets. Journal of cheminformatics, 5(1), 41.
    """

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_protfp_codebook(self._aa_list)
