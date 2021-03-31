"""Entrypoint for Jupyter kernels submited via WLMs,
such as SLURM or PBS Pro"""

from .ipykernel_wlm import main  # noqa

try:
    from ._version import VERSION as __version__
except ImportError:
    __version__ = "0.0.dev"

__author__ = "Bright Computing Holding BV"
__url__ = "http://brightcomputing.com"
