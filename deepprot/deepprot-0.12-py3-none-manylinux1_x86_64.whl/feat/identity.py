"""
identity
~~~
Identity one-hot encoding.
"""

import numpy as np
from typing import Dict, Iterable

from deepprot.feat.featurizer import DescriptorFeaturizer


def _generate_identity_codebook(aa_list: Iterable[str]) -> Dict[str, str]:
    identity = {}
    for i, aa in enumerate(aa_list):
        ohe = np.zeros(len(aa_list))
        ohe[i] = 1
        identity[aa] = np.squeeze(ohe)
    # Remove singleton dimensions that perturbe shape.
    return identity


class Identity(DescriptorFeaturizer):

    """One-hot encoding / identity vector representation of AA sequence."""

    def __init__(self, fixed_dim=False):
        super().__init__(fixed_dim)
        self._codebook = _generate_identity_codebook(self._aa_list)
