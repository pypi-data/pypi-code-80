"""The dataset module defines the core `Dataset` class.

A `Dataset` should be instantiated from any filetype, with the same
developer facing API and everything should "just work".

Example:
    You can instantiate `Dataset`s with various levels of parameterization.
    literal blocks::

        antibodies = deepprot.data.Dataset("cancer_cure.csv")

        # Alternatively...
        antibodies = deepprot.data.Dataset("cancer_cure.csv", X="seq", y="affinity")

Sensible defaults for parsing different filetypes are included out-of-the-box.
Internal are of course easily parameterized via kwargs.

Todo:
    * Support for `.json`
"""

import pickle
import math
import copy
import os

import torch
import pandas as pd

from deepprot.feat import Featurizer


class Dataset(torch.utils.data.IterableDataset):

    """Dataset is the core data representation in DeepProt.

    The class should be flexibly instantiated from any filetype or in-memory
    primitive. Downstream interactions with `DataLoader`s or `Model`s are then
    guranteed to play nice.

    Attributes:
        X (:obj:`Iterable`): Core datapoints
        y (:obj:`Iterable`, optional): Optional labels (one-to-one mapping)
    """

    def __init__(self, file_path: str, X: str = None, y: str = None):
        """Dataset should be consistently instantiated for all filetypes.

        Args:
            file_path: Location of data file.
            X (optional): Metadata annotation (ie. csv column header) to
                identitfy X.
            y (optional): Metadata annotation (ie. csv column header) to
                identitfy y.
        """
        super(Dataset).__init__()

        # Parse filetype and conditionally instantiate.
        _, ftype = os.path.splitext(file_path)

        if ftype == ".pkl":
            with open(file_path, "rb") as handle:
                raw_map = pickle.load(handle)

            self._X, self._y = list(zip(*raw_map.items()))

        else:
            # When reading the csv, run sensible type conversions.
            df = pd.read_csv(file_path)

            # TODO: log default label picking
            self._X_label = X if X else df.columns[0]
            self._y_label = y if y else df.columns[1]

            # TODO: internal X,y always a generic python iterator...
            self._X = df[self._X_label].tolist()
            self._y = df[self._y_label].tolist()

        # Indicates of X has a variable length - cache for computed attribute.
        self._featurizer = None
        self._is_fixed = None
        self.start = 0
        self.end = len(self._y)

    def describe(self) -> pd.DataFrame:
        """Return semantic description of `Dataset`.

        Returns:
            Description to stdout.
        """

        return self.to_df().describe()

    def to_df(self) -> pd.DataFrame:
        """Exports `Dataset` to a `pandas` DataFrame."""

        return pd.DataFrame({self._X_label: self._X, self._y_label: self._y})

    def _add_featurizer(
        self, featurizer: Featurizer
    ) -> torch.utils.data.IterableDataset:
        """Private ~ intended for DeepProt internals. """

        alias = copy.deepcopy(self)
        alias._featurizer = featurizer
        return alias

    @property
    def is_fixed(self) -> bool:
        """Private ~ intended for DeepProt internals. """

        if type(self._is_fixed) is bool:
            return self._is_fixed

        first_len = len(self._X[0])
        self._is_fixed = all([len(x) == first_len for x in self._X])
        return self._is_fixed

    def _get_data_dimensions(self):
        """Private ~ intended for DeepProt internals. """

        if self.is_fixed:

            if type(self._X[0]) is str:
                x_shape = (len(self._X[0]),)
            else:
                x_shape = self._X[0].shape

            if self._featurizer:
                print("feat: ", [i.shape for i in self._featurizer(self._X[0])])
                feat_shape = self._featurizer(self._X[0]).shape
            else:
                feat_shape = None

        # Represent variable dimension as -1 as is convention.
        else:

            def variable_rep(x):
                shape = [-1 for i in range(len(x))]
                shape[-1] = x[-1]
                return shape

            if type(self._X[0]) is str:
                x_shape = (-1,)
            else:
                x_shape = variable_rep(self._X[0].shape)

            if self._featurizer:
                feat_shape = variable_rep(self._featurizer(self._X[0]).shape)
            else:
                feat_shape = None

        y = self._y[0]
        y_shape = (1,) if type(y) is float else y.shape
        categories = max(self._y[0]) if type(y) is not float else None

        return (x_shape, feat_shape, y_shape, categories)

    def __iter__(self):

        worker_info = torch.utils.data.get_worker_info()

        # Single-process data loading, return the full iterator.
        if worker_info is None:
            iter_start = self.start
            iter_end = self.end

        else:
            # Map sets of data to dedicated workers.
            per_worker = int(
                math.ceil((self.end - self.start) / float(worker_info.num_workers))
            )
            worker_id = worker_info.id
            iter_start = self.start + worker_id * per_worker
            iter_end = min(iter_start + per_worker, self.end)

        # TODO: Figure out how to reconcile lazy loading and batched
        # featurization.
        if self._featurizer:
            X = self._featurizer.featurize(self._X[iter_start : iter_end + 1])
        else:
            X = self._X[iter_start : iter_end + 1]

        return iter(zip(X, self._y[iter_start : iter_end + 1],))

    def __repr__(self) -> str:

        return (
            pd.DataFrame({self._X_label: self._X, self._y_label: self._y})
            .head()
            .to_string()
        )

    def __unicode__(self) -> str:

        return (
            pd.DataFrame({self._X_label: self._X, self._y_label: self._y})
            .head()
            .to_string()
        )
