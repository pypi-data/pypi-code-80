try:
    from project._version import version as __version__
except ImportError:
    __version__ = "0.0.1-not-installed"
