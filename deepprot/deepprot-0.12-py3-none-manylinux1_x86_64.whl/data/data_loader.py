"""The data_loader module defines the core `DataLoader` class.

A `DataLoader` takes in a `Datset` and performs any necessary transforms,
featurizations, training batching, etc.

When used with DeepProt workflows, everything should just work.

Example:

    literal blocks::

        dl = deepprot.data.DataLoader(antibodies)

        # Alternatively...
        dl = deepprot.data.DataLoader(antibodies,
            featurizer=deepprot.feat.KideraFactors())

        # Easily batch for downstream training...
        dl = deepprot.data.DataLoader(antibodies, batch_size=64)
"""

import torch

from deepprot.data import Dataset
from deepprot.feat import Featurizer


class DataLoader(object):

    """The core class for manipulating `Dataset`s.

    Some core features:

        * Data parallelized and multi-process loading with a keyword.
        * Sensible batch collation for variable input (non-padded) data.
        * Lazy featurization and transformations

    By deferring `Dataset` manipulations (featurization, transforms, batching,
    etc.) to when they are needed (ie. lazy evaluation) we can save potentially
    wasteful computation and create clean seperation between raw data
    primitives and their various manipulations.

    TODO: Provide description to overload collate_fn and multi-processing
    internals.
    """

    def __init__(
        self,
        dataset: Dataset,
        batch_size: int = None,
        num_workers: int = 0,
        featurizer: Featurizer = None,
    ):
        """DataLoader should be instantiated easily from a Dataset and friends.

        Args:
            datset: Location of data file.
            batch_size (optional): Batch size (number of samples in a single
                forward pass) for training.
            num_workers (optional): Specify number of parallel threads for
                multi-process loading - defaults to 0.
            featurizer (optional): A `Featurizer` object.
        """

        # Developer notes:

        # To decouple "loading" from "data" - copies of the underlying Dataset
        # parameterized with the appropriate featurizer will be created
        # liberally...

        # TODO: multi-process collation
        def collate_fn(batch):
            if len(batch) == 1:
                return [[batch[0][0]], [batch[0][1]]]
            return list(zip(*batch))

        # TODO: Inject a custom batch collate_fn if input is variable.
        # Detect this automatically for the developer by making a copy of the
        # iterator and manually checking if dimensions are variable.
        # There's probably a better way to do this...

        collate = collate_fn if not dataset.is_fixed and batch_size else None

        self._dataset = dataset._add_featurizer(featurizer)
        self.data_dims = self._dataset._get_data_dimensions()
        self._dataloader = torch.utils.data.DataLoader(
            self._dataset,
            batch_size=batch_size,
            num_workers=num_workers,
            collate_fn=collate,
        )

        # TODO: want this to stick around?
        self._featurizer = featurizer

    def __iter__(self):

        # Pytorch's dataloader is an iterable generator.
        # Unwrap what we need...
        # https://stackoverflow.com/questions/64577138/implement-iter-and-next-in-different.

        return self._dataloader.__iter__()
