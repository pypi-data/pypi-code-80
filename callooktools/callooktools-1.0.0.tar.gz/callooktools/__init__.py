"""
callooktools
---
callook.info API interface in Python

Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""

from importlib.util import find_spec

from .__info__ import __version__  # noqa: F401

from .callooktools import CallookError, CallookCallsignData, CallookAbc  # noqa: F401

if find_spec("requests"):
    from .callooksync import CallookSync  # noqa: F401
if find_spec("aiohttp"):
    from .callookasync import CallookAsync  # noqa: F401
if not find_spec("requests") and not find_spec("aiohttp"):
    raise ModuleNotFoundError("At least one of requests or aiohttp needs to be installed to use callooktools")
