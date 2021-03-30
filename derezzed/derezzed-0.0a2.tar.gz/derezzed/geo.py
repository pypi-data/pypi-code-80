"""Place geographic locations into regions.

Classes:

    GeoRegionChain

Functions:

    read_geojson(str) -> shapely.geometry.base.BaseGeometry

"""

import json
from collections import OrderedDict
from typing import Dict
from typing import List

from shapely.geometry import GeometryCollection  # type: ignore
from shapely.geometry import Point  # type: ignore
from shapely.geometry import shape  # type: ignore
from shapely.geometry.base import BaseGeometry  # type: ignore


def read_geojson(path: str) -> BaseGeometry:
    """Read a `GeoJSON <https://geojson.org/>`_ file.

    The file is read from a given path and will have all features merged into a
    `Shapely <https://shapely.readthedocs.io/>`_ geometry.

    :param path: Filesystem path to GeoJSON file
    """
    with open(path) as input_file:
        features = json.load(input_file)["features"]
        result = None
        for geom in GeometryCollection(
              [shape(feature["geometry"]).buffer(0) for feature in features]):
            result = geom if not result else result | geom
        return result


class GeoRegionChain:
    """
    Reduces the resolution of a point to a geographic region.

    Region configuration must be passed as a list of dictionaries, with each
    dictionary having a "name" and "path" key. For example:

    >>> from derezzed.geo import GeoRegionChain
    >>> regions = [
    ...   {"name": "ma", "path": "../examples/ma.geojson"},
    ...   {"name": "usa", "path": "../examples/usa.geojson"},
    ... ]
    >>> g = GeoRegionChain(regions)
    >>> g
    <GeoRegionChain ma,usa>

    The order of the configuration elements matters. If more than one geometry
    would contain a point, the first entry in the list will be the name that
    is returned.

    :param region_config: Geographic region configuration
    """

    _regions: "OrderedDict[str, BaseGeometry]"

    def __init__(self, region_config: List[Dict[str, str]]):
        """Construct new georegions from configuration."""
        self._regions = OrderedDict()
        for region in region_config:
            self._regions[region["name"]] = read_geojson(region["path"])

    def match(self, lat: float, lon: float) -> str:
        """Place a point into a region and return that region name.

        If no region matches, "other" is returned.

        >>> gb.region(42.360092, -71.094162) # MIT, Massachusetts
        'ma'
        >>> gb.region(38.897675, -77.036530) # White House, Washington
        'usa'
        >>> gb.region(45.421532, -75.697189) # Ottawa, Canada
        'other'

        :param lat: Decimal latitude
        :param lon: Decimal longitude
        """
        point = Point(lon, lat)
        for name in self._regions:
            if point.within(self._regions[name]):
                return name
        return "other"

    def __repr__(self) -> str:
        """Return representation of self."""
        return "<GeoRegionChain " + ",".join(self._regions.keys()) + ">"
