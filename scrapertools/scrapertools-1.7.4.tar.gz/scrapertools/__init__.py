__version__ = "1.7.4"
__author__ = "UltrafunkAmsterdam"
__url__ = "https://github.com/ultrafunkamsterdam/scrapertools"
__license__ = "GPL3.0 License"
__author_email__ = "info@ultrafunk.nl"
__description__ = "scraping for humans"


from ._ua import (
    GENERIC_CURL,
    GENERIC_WINDOWS,
    GENERIC_GOOGLEBOT,
    GENERIC_MACOS,
    GENERIC_MOBILE,
    GENERIC_WEBKIT,
)

from ._util import load_state, save_state, fetch
from . import _util as util
