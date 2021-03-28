import os

from ._version import __version__

_commit_tag = os.environ.get("CI_COMMIT_TAG", "")
_short_sha = os.environ.get("CI_COMMIT_SHORT_SHA", "")

if _commit_tag:
    if _commit_tag != __version__:
        raise RuntimeError(
            "Attempting CI build with mismatching package version ({}) "
            "and CI tag version ({}).".format(__version__, _commit_tag)
        )
elif _short_sha:
    # PEP 440 compliant way to include commit SHA in package version.
    # We use "post" instead of "pre", because we want this version to be
    # considered newer, than the previous release version.
    # (1.0.0.post0+... > 1.0.0 > 1.0.0.pre0+...)
    __version__ = __version__ + ".post0+" + _short_sha
