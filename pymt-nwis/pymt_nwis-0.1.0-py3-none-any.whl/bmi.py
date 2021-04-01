from __future__ import absolute_import

import pkg_resources
from nwis import BmiNwis as Nwis

Nwis.__name__ = "Nwis"
Nwis.METADATA = pkg_resources.resource_filename(__name__, "data/Nwis")

__all__ = [
    "Nwis",
]
