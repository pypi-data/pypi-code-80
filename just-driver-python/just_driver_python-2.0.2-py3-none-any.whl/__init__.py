from .api import connect

VERSION = (2, 0, 0)
__version__ = '.'.join(str(x) for x in VERSION)

__all__ = ['connect']
