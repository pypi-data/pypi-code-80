import rdata
import os
from typing import Dict

import numpy as np

from deepprot.utils.constants import aa_list


def descriptor_from_rdata(descriptor_name: str) -> Dict[str, np.array]:
    """Construct a descriptor codebook for a `DescriptorFeaturizer`.

    Matrices are vendored from the
    [Peptides](https://www.rdocumentation.org/packages/Peptides/versions/2.4.3)
    R package. More information can be found
    [here](https://www.rdocumentation.org/packages/Peptides/versions/2.4.3/topics/aaDescriptors).

    Args:
        descriptor_name (str): The name or key corresponding

    Returns:
        dict: A mapping from residues to feature vectors.

    """

    def _load_from_rdata(fname: str):
        parsed = rdata.parser.parse_file(fname)
        converted = rdata.conversion.convert(parsed)
        return converted

    # Resolve absolute path to vendored binary.
    curr_dir, _ = os.path.split(os.path.abspath(__file__))
    fp = os.path.join(curr_dir, "../_vendor/AAdata.Rdata")
    raw_df = _load_from_rdata(fp)
    descriptor_df = raw_df["AAdata"][descriptor_name]

    codebook = {char: [] for char in aa_list}
    for descriptor in descriptor_df.keys():
        for i, feature in enumerate(descriptor_df[descriptor]):
            codebook[aa_list[i]].append(feature)

    # Convert descriptors to numpy arrays.
    codebook = {aa: np.array(codebook[aa]) for aa in codebook}

    return codebook
