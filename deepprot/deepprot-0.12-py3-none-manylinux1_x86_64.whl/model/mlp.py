"""Defines a generic MLP (Multi-layer perceptron) head.

A `MLP` model is a modular building block or a stand-alone model.

It's architecture is constructed at run-time, adapting dimensions and training
dynamics to information provided by the `DataLoader`, similar to JIT
compilation.

When used with DeepProt workflows, everything should just work.

Example:

    literal blocks::

        antibodies = deepprot.data.Dataset("cancer_cure.csv")
        dl = deepprot.data.DataLoader(antibodies, featurizer=deepprot.feat.KideraFactors())
        mlp = MLP()
        mlp.fit(dl)
"""
import torch
from torch import nn
import torch.nn.functional as F

from deepprot.model import TorchModel
from deepprot.data import DataLoader


class MLP(TorchModel):

    """A multilayer NN standalone model or modular building block."""

    def __init__(self):
        super().__init__()
        self._mlp = None

    @staticmethod
    def _construct_mlp(dl: DataLoader) -> nn.Module:
        """Private ~ intended for DeepProt internals. """

        _, feat_x_shape, y_shape = dl.data_dims

        fixed_dim = feat_x_shape[-1]
        output_dim = y_shape[0]

        # TODO: Raise exception if variable input - cannot handle
        if len(feat_x_shape) > 2:
            raise ValueError("Attempting to apply linear operator to 2D tensor.")

        return nn.Sequential(
            nn.Linear(fixed_dim, 100), nn.ReLU(), nn.Linear(100, output_dim), nn.ReLU()
        )

    def forward(self, x):
        """Defines a forward pass.

        TODO: typing

        Args:
            x: Single sample for inference.
        """
        x = torch.tensor(x).float()
        return self._mlp(x)

    def training_step(self, batch, batch_idx):
        """Defines a pytorch training loop.

        TODO: typing

        Args:
            batch: Tuple containing sample and label (opt.) pair.
            batch_idx: Batch index in an epoch.
        """
        x, y = batch
        x = torch.unsqueeze(x.float(), dim=0)
        y = torch.unsqueeze(torch.tensor(y), dim=0)

        y_hat = self._mlp(x)
        y = torch.unsqueeze(torch.tensor(y), dim=0)
        loss = F.mse_loss(y_hat, y)
        return loss

    def evaluate(self, arg1):
        """DeepProt interface for inference"""

        raise NotImplementedError

    def fit(self, train_loader: DataLoader, val_loader: DataLoader = None):
        """DeepProt interface for training.

        Args:
            train_loader: A DataLoader to train with.
            val_loader: A DataLoader to validate against.
            epochs: Maximum number of epochs
                (full passes through a DataLoader) for training.

        TODO: Various training utilities.
        """
        self._dataloader = train_loader
        self._mlp = self._construct_mlp(train_loader)

        super().fit(train_loader, val_loader)
