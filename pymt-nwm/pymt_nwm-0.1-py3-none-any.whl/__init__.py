#! /usr/bin/env python
import pkg_resources

__version__ = pkg_resources.get_distribution("pymt_nwm").version


from .bmi import Nwm

__all__ = [
    "Nwm",
]
