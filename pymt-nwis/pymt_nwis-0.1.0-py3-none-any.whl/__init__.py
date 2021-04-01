#! /usr/bin/env python
import pkg_resources

__version__ = pkg_resources.get_distribution("pymt_nwis").version


from .bmi import Nwis

__all__ = [
    "Nwis",
]
