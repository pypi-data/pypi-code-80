from abc import ABCMeta, abstractmethod
from typing import Any, Iterable
import logging
import re

import numpy as np
from transformers import AutoTokenizer, AutoModel, pipeline

from deepprot.utils.constants import aa_list

logger = logging.getLogger(__name__)


class Featurizer(metaclass=ABCMeta):
    """Abstract Base Class that defines an interface for featurizing data.

    Defines a data model that is easily extensible vis-a-vis
    [open-closed](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)
    philosophy.

    This is thus a formal implementation of an object interface. Developers
    need only to implement the `featurize` method (without explicit
    inheritance) in a custom object and their
    code will play nicely with the extended deepProt ecosystem.
    """

    @abstractmethod
    def featurize(self, X: Iterable[Any], log: bool = False) -> Iterable[Any]:
        """Featurize data.

        TODO: Note that every returned data type will contain the batch
        dimension at axis x=0 to avoid confusion.

        Args:
            X (Iterable[Any]): An iterator that contains data.
            log (bool): A flag to indicate logging during featurization.

        Returns:
            Iterable[Any]: An iterator that contains featurized data.
        """
        raise NotImplementedError

    @abstractmethod
    def _featurize(self, x: Any) -> Any:
        """Featurize a single datapoint.

        Args:
            x (Any): A single datapoint.

        Returns:
            Any: A single featurized datapoint.
        """
        raise NotImplementedError

    def __call__(self, datapoints: Iterable[Any], log: bool = False):
        """Featurize data.

        Args:
            X (Iterable[Any]): An iterator that contains data.
            log (bool): A flag to indicate logging during featurization
        """

        return self.featurize(datapoints, log)

    @classmethod
    def __subclasshook__(cls, C):
        """Asserts that objects implementing ABC have correct behavior."""
        if cls is Featurizer:
            # https://stackoverflow.com/questions/2010692/what-does-mro-do
            if any("featurize" and "_featurize" in B.__dict__ for B in C.__mro__):
                return True
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        """Memory representation.

        Returns:
          str: Memory representation of self.
        """

        raise NotImplementedError

    @abstractmethod
    def __unicode__(self) -> str:
        """String representation

        Returns:
          str: String representation of self.
        """

        raise NotImplementedError


class DescriptorFeaturizer(Featurizer):
    """ TODO: simple codebook mapping
    """

    def __init__(self, fixed_dim=False):
        """A DescriptorFeaturizer is defined by its codebook
        """
        self._codebook = None
        self._aa_list = aa_list
        self._fixed_dim = fixed_dim

    def featurize(self, X: Iterable[str], log: bool = False) -> Iterable[np.ndarray]:
        """Apply an identity one-hot encoding over an amino acid code.

        Args:
            X (Iterable[Any]): An iterator that contains data.
            log (bool): A flag to indicate logging during featurization.

        Returns:
            Iterable[Any]: An iterator that contains featurized data.
        """

        # If single input and string, prevent conversion to char list.
        if type(X) is not str:
            X = list(X)
        else:
            X = [X]

        featurized_X = []
        # Check if datapoints are the same length
        is_fixed, curr_length = [True, len(X[0])]

        for i, x in enumerate(X):

            if is_fixed and len(x) != curr_length:
                is_fixed = False

            try:
                featurized_X.append(self._featurize(x))
            except Exception as e:
                print(e)
                logger.warning("Failed to featurize datapoint %d. Appending None.")
                featurized_X.append(None)

        # Fixed length descriptors can be massaged into numpy objects.
        return np.array(featurized_X) if is_fixed else featurized_X

    def _featurize(self, x: Any) -> np.ndarray:
        """Featurize a single datapoint.

        Args:
            x (Any): A single datapoint.

        Returns:
            Any: A single featurized datapoint.
        """

        # Assume each residue descriptor is fixed length.
        code_len = len(list(self._codebook.values())[0])
        full_feature = np.zeros((len(x), code_len))

        for i, residue in enumerate(x):
            if residue in self._codebook:
                full_feature[i] = self._codebook[residue]
            else:
                #  TODO: deal with malformed residues / diff. MSA reps. #
                full_feature[i] = np.zeros((1, code_len))

        if self._fixed_dim:
            full_feature = np.mean(full_feature, axis=0)

        return full_feature

    def __repr__(self):
        return str(self._fixed_dim)

    def __unicode__(self):
        return "todo"


class EmbeddingFeaturizer(Featurizer):
    """ TODO: extracts some feature vector from a trained machine learning model

    # Use huggingfaces default cache in `~/.config/transformers` for now.
    """

    @staticmethod
    def _init_extraction_pipeline(model_name: str):
        """"""

        tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=False)
        model = AutoModel.from_pretrained(model_name)
        extraction_pipeline = pipeline(
            "feature-extraction", model=model, tokenizer=tokenizer
        )

        return tokenizer, model, extraction_pipeline

    def featurize(self, X: Iterable[str], log: bool = False) -> Iterable[np.ndarray]:
        """Embed a set of sequences

        Args:
            X (Iterable[Any]): An iterator that contains data.
            fixed_dim (bool): Indicate if embeddings should be fixed in dimension / pooled
                across the variable axis
            log (bool): A flag to indicate logging during featurization.

        Returns:
            Iterable[Any]: An iterator that contains featurized data.
        """

        # If single input and string, prevent conversion to char list.
        if type(X) is not str:
            X = list(X)
        else:
            X = [X]

        featurized_X = []
        # Check if datapoints are the same length
        is_fixed, curr_length = [True, len(X[0])]

        for i, x in enumerate(X):

            if is_fixed and len(x) != curr_length:
                is_fixed = False

            try:
                featurized_X.append(self._featurize(x))
            except Exception as e:
                print(e)
                logger.warning("Failed to featurize datapoint %d. Appending None.")
                featurized_X.append(None)

        # Fixed length descriptors can be massaged into numpy objects.

        return np.array(featurized_X) if is_fixed else featurized_X

    def _featurize(self, x: str) -> np.ndarray:
        """Embed a single sequence.

        Args:
            x (str): A single sequence

        Returns:
            Any: A single featurized (embedded) datapoint.
        """

        seq_len = len(x)

        # "GSG" -> "G S G"
        seq = " ".join(list(x))
        # Replace all generic or unresolved residues with 'X' for NLP vocab.
        seq = re.sub(r"[UZOB]", "X", seq)

        np_rep = np.array(self._extraction_pipeline(seq))
        embedding = np.squeeze(np_rep, axis=0)
        # Remove special (PAD + CLS) tokens from BERT.
        embedding = embedding[1 : seq_len + 1]

        return embedding

    def __repr__(self):
        return "todo"

    def __unicode__(self):
        return "todo"
