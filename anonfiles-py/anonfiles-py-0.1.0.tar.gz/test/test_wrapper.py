import pytest

from anonfiles import AnonFiles


@pytest.fixture()
def anonfile():
    """Return AnonFiles object."""
    return AnonFiles()


# NOTE: file id used really exists
@pytest.mark.parametrize(
    "id, status",
    [("d9e3l3ofub", True), ("justnonexistentid", False)],
)
def test_info(anonfile, id, status):
    info = anonfile.info(id)
    assert info.status == status