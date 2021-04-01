from anonfiles.anonfiles import BayFiles
import pytest

from anonfiles import AnonFiles, BayFiles


@pytest.fixture()
def anonfile():
    """Return AnonFiles object."""
    return AnonFiles()


@pytest.fixture()
def bayfile():
    """Return BayFiles object."""
    return BayFiles()


# NOTE: file ids used really exists
@pytest.mark.parametrize(
    "anonid, status",
    [("d9e3l3ofub", True), ("justnonexistentid", False)],
)
def test_anonfile_info(anonfile, anonid, status):
    info = anonfile.info(anonid)
    assert info.status == status


# NOTE: file ids used really exists
@pytest.mark.parametrize(
    "bayid, status", [("zcL5n4o4u6", True), ("justnonexistentid", False)]
)
def test_bayfile_info(bayfile, bayid, status):
    info = bayfile.info(bayid)
    assert info.status == status