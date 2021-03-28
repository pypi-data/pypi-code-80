__version__ = "1.2.2"
__author__ = "UltrafunkAmsterdam"

from ._ua import (
    GENERIC_CURL,
    GENERIC_WINDOWS,
    GENERIC_GOOGLEBOT,
    GENERIC_MACOS,
    GENERIC_MOBILE,
    GENERIC_WEBKIT,
)
from ._util import load_state, save_state, fetch, Session
