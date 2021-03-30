import unittest

from pkg_resources import resource_filename

from derezzed.geo import GeoRegionChain

class TestGeoRegionChain(unittest.TestCase):
    chain: GeoRegionChain

    def setUp(self) -> None:
        config = [
            {"name": "ma", "path": resource_filename("derezzed.tests", "ma.geojson")},
            {"name": "usa", "path": resource_filename("derezzed.tests", "usa.geojson")},
        ]
        self.chain = GeoRegionChain(config)

    def test_geo_point_ma(self) -> None:
        # MIT, Massachusetts
        assert self.chain.match(42.360092, -71.094162) == "ma"

    def test_geo_point_usa(self) -> None:
        # White House, Washington
        assert self.chain.match(38.897675, -77.036530) == "usa"

    def test_geo_point_other(self) -> None:
        # Ottawa, Canada
        assert self.chain.match(45.421532, -75.697189) == "other"
