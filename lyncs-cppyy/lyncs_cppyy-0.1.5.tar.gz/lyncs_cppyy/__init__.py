"""
Cppyy interface for Lyncs

In this package we provide some additional tools for the usage of
[cppyy](https://cppyy.readthedocs.io/en/latest/) in the Lyncs API.
"""

__version__ = "0.1.5"

from cppyy import nullptr, cppdef, gbl, include
from .lib import *
from . import ll

# including and aliasing
include(__path__[0] + "/utils.h")
make_shared = gbl.lyncs_cppyy_make_shared
