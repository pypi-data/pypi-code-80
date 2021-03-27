__version__ = "0.1.1"
from .get_pwbrowser import get_pwbrowser
from .get_pwbrowser_async import get_pwbrowser as get_pwbrowser_async

# import nest_asyncio
# nest_asyncio.apply()

__all__ = [
    "get_pwbrowser",
    "get_pwbrowser_async",
]
