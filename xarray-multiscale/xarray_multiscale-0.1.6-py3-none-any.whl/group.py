from collections.abc import MutableMapping
from xarray import DataArray

class Group(MutableMapping[str, DataArray]):
    