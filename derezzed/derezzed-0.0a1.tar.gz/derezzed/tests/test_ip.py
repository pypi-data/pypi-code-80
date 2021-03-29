import unittest

from pkg_resources import resource_filename

from derezzed.ip import GeoIPCity

class TestGeoIPCity(unittest.TestCase):
    _city: GeoIPCity

    def setUp(self) -> None:
        self._city = GeoIPCity(resource_filename("derezzed.tests", "GeoIP2-City-Test.mmdb"))

    def test_ip_point_asia(self) -> None:
        assert self._city.lookup_point("202.196.224.1") == (13, 122)

    def test_ip_point_london(self) -> None:
        assert self._city.lookup_point("81.2.69.142") == (51.5142, -0.0931)
