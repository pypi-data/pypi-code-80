__version__ = "1.0.0"
__author__ = "UltrafunkAmsterdam"

from ._ua import (
    GENERIC_CURL,
    GENERIC_WINDOWS,
    GENERIC_GOOGLEBOT,
    GENERIC_MACOS,
    GENERIC_MOBILE,
    GENERIC_WEBKIT,
)
from ._util import load_session, save_session, fetch, Session
