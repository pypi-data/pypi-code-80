# Copyright (c) 2021, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""normetapi - A library for interacting with the MET Norway Weather API."""
from .version import VERSION as __version__
from .api import location_forecast, weathericon, nowcast
