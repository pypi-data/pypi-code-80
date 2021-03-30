from ipaddress import IPv4Address
from typing import Optional
from typing import Tuple
from typing import Union

import geoip2.database


class GeoIPCity:
    _reader: geoip2.database.Reader

    def __init__(self, db_path: str):
        self._reader = geoip2.database.Reader(db_path)

    def lookup_point(
        self,
        ip: Union[str,
                  IPv4Address]) -> Tuple[Optional[float], Optional[float]]:
        response = self._reader.city(str(ip))
        return (response.location.latitude, response.location.longitude)

    def lookup_country(self, ip: Union[str, IPv4Address]) -> Optional[str]:
        response = self._reader.city(str(ip))
        return response.country.iso_code
