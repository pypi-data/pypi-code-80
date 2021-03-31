from nztm.lib import NZTMToWGS84
from nztm.tuples import NZTMCoordinates, WGS84Coordinates
from nztm.util import NZTMUtil


def NZTMToWGS64(
        nztmCoordinates: NZTMCoordinates, unit=NZTMUtil.DEG
) -> WGS84Coordinates:
    latRad, longRad = NZTMToWGS84.NZTMToGeod(
        nztmCoordinates.easting, nztmCoordinates.northing
    )
    coord = WGS84Coordinates(latitude=latRad, longitude=longRad, unit=NZTMUtil.RAD)
    if unit == NZTMUtil.DEG:
        coord = NZTMUtil.WGS84RadianToDegree(coord)
    return coord


def WGS64toNZTM(wgs64Coordinates: WGS84Coordinates, precision=2) -> NZTMCoordinates:
    easting, northing = NZTMToWGS84.GeodToNZTM(
        wgs64Coordinates.longitude, wgs64Coordinates.latitude
    )
    easting, northing = round(easting, precision), round(northing, precision)
    return NZTMCoordinates(easting=easting, northing=northing)
