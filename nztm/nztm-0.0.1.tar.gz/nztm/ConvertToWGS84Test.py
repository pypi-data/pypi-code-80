import unittest
import collections

from ddt import ddt, data

# Create a format for the test data coordinates and benchmarks
from nztm import NZTMToWGS64, NZTMCoordinates, WGS64toNZTM, NZTMUtil

TestPair = collections.namedtuple("TestPair", ["output", "benchmark"])


@ddt
class NZTMTests(unittest.TestCase):

    # Convert some coordinates (left) to test against government conversions (right)
    # Benchmarks are generated in Degrees, Minutes, Seconds using:
    # https://www.linz.govt.nz/data/geodetic-services/coordinate-conversion/online-conversions
    # If you plan to add values, note that the site actually outputs N/S where E/W should be used and vice versa
    @data(
        NZTMCoordinates(1576041.15, 6188574.24),
        NZTMCoordinates(1576542.01, 5515331.05),
        NZTMCoordinates(1307103.22, 4826464.86),
    )
    def testTwoWayConversion(self, nztmCoordinates: NZTMCoordinates):
        eastingFailureMsg = "conversion easting is not correct to 4 decimal places"
        northingFailureMsg = "conversion northing is not correct to 2 decimal places"

        wgs64 = NZTMToWGS64(nztmCoordinates)
        wgs64 = NZTMUtil.WGS84DegreeToRadian(wgs64)
        nztmOutput = WGS64toNZTM(wgs64, precision=2)

        # Test easting
        self.assertEqual(nztmOutput.easting, nztmCoordinates.easting, eastingFailureMsg)

        # Test northing
        self.assertEqual(
            nztmOutput.northing, nztmCoordinates.northing, northingFailureMsg
        )
