"""Defines a generic CNN head.

A `CNN` model is a modular building block or a stand-alone model.

It's architecture is constructed at run-time, adapting dimensions and training
dynamics to information provided by the `DataLoader`, similar to JIT
compilation.

When used with DeepProt workflows, everything should just work.

Example:

    literal blocks::

        antibodies = deepprot.data.Dataset("cancer_cure.csv")
        dl = deepprot.data.DataLoader(antibodies, featurizer=deepprot.feat.KideraFactors())
        cnn = CNN()
        cnn.fit(dl)
"""

import torch
from torch import nn
from torch.nn.utils.weight_norm import weight_norm
import pytorch_lightning as pl

from deepprot.model import TorchModel
from deepprot.data import DataLoader


class CNN(TorchModel):

    """A Convolutional NN standalone model or modular building block."""

    def __init__(self):
        """Necessary parameters will be pulled at run-time.

        TOOD: intuitive kwargs for developers.
        """
        super().__init__()

        self._cnn = None
        self.loss = nn.CrossEntropyLoss()
        self.accuracy = pl.metrics.Accuracy()

    @staticmethod
    def _construct_cnn_head(dl: DataLoader) -> nn.Module:
        """Private ~ intended for DeepProt internals. """

        _, feat_x_shape, y_shape, categories = dl.data_dims

        if len(feat_x_shape) < 3:
            # TODO: develop sensible error.
            raise ValueError(
                "Cannot convolve over tensor of shape {feat_x_shape} - not enought dimensions."
            )

        if not categories:
            # TODO: develop sensible error.
            raise ValueError(
                "Classification head does not yet support non-reconstruction tasks."
            )

        static_dim = feat_x_shape[-1]
        out_dim = y_shape[0]

        class _CNNHead(nn.Module):
            def __init__(
                self, in_dim: int, hid_dim: int, out_dim: int, dropout: float = 0.0
            ):
                super().__init__()
                self.main = nn.Sequential(
                    weight_norm(nn.Conv1d(in_dim, hid_dim, 5, padding=2), dim=None),
                    nn.ReLU(),
                    nn.Dropout(dropout, inplace=True),
                    weight_norm(nn.Conv1d(hid_dim, out_dim, 3, padding=1), dim=None),
                    nn.Softmax(dim=-2),
                )

            def forward(self, x):
                x = x.transpose(1, 2)
                x = self.main(x)
                return x

        return _CNNHead(static_dim, 512, out_dim)

    def forward(self, x):
        """Defines a forward pass.

        TODO: typing

        Args:
            x: Single sample for inference.
        """

        return self._cnn(x)

    def training_step(self, batch, batch_idx):
        """Defines a pytorch training loop.

        TODO: typing

        Args:
            batch: Tuple containing sample and label (opt.) pair.
            batch_idx: Batch index in an epoch.
        """
        x, y = batch

        x = torch.unsqueeze(x.float(), axis=0)
        pred = self._cnn(x)
        labels = torch.unsqueeze(torch.tensor(y).long(), dim=0)

        cross_entropy = self.loss(pred, labels)
        self.log("acc", self.accuracy(pred, labels), on_step=True)
        return cross_entropy

    def evaluate(self):
        """DeepProt interface for inference"""

        raise NotImplementedError

    def fit(
        self, train_loader: DataLoader, val_loader: DataLoader = None, epochs: int = 10
    ):
        """DeepProt interface for training.

        Args:
            train_loader: A DataLoader to train with.
            val_loader: A DataLoader to validate against.
            epochs: Maximum number of epochs
                (full passes through a DataLoader) for training.

        TODO: Various training utilities.
        """

        self._cnn = self._construct_cnn_head(train_loader)
        super().fit(train_loader, val_loader, epochs=epochs)
