from __future__ import absolute_import

import pkg_resources
from nwm import BmiNwmHs as Nwm

Nwm.__name__ = "Nwm"
Nwm.METADATA = pkg_resources.resource_filename(__name__, "data/Nwm")

__all__ = [
    "Nwm",
]
