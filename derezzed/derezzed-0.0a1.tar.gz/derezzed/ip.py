from ipaddress import IPv4Address
from typing import Tuple
from typing import Union

import geoip2.database


class GeoIPCity:
    _reader: geoip2.database.Reader

    def __init__(self, db_path: str):
        self._reader = geoip2.database.Reader(db_path)

    def lookup_point(self, ip: Union[str, IPv4Address]) -> Tuple[float, float]:
        response = self._reader.city(str(ip))
        return (response.location.latitude, response.location.longitude)

    def lookup_country(self, ip: Union[str, IPv4Address]) -> str:
        response = self._reader.city(str(ip))
        return response.country.iso_code
