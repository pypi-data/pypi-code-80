# type: ignore[attr-defined]
"""Miscellaneous functions for working with the Earth Engine Python API."""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
