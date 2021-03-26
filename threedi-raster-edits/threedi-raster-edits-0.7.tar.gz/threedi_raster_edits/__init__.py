try:
    from osgeo import ogr

    ogr  # Pyflakes
except ImportError:
    raise (
        """ ERROR: Could not find the GDAL/OGR Python library bindings.
               On anaconda, use conda install gdal >= 3.2.0
               otherwise look at https://pypi.org/project/GDAL/"""
    )

# gis
from .gis.raster import Raster
from .gis.rastergroup import RasterGroup
from .gis.vector import Vector
from .gis.linestring import LineString, MultiLineString
from .gis.polygon import Polygon, MultiPolygon
from .gis.point import Point, MultiPoint

# Threedi
from .threedi.rastergroup import ThreediRasterGroup
from .threedi.rastergroup import retrieve_soil_conversion_table
from .threedi.rastergroup import retrieve_landuse_conversion_table


# Lizard
from .lizard.rextract import RasterExtraction
from .lizard import uuid as UUID


# Pyflakes
Raster
RasterGroup
Vector
LineString
MultiLineString
Polygon
MultiPolygon
Point
MultiPoint
ThreediRasterGroup
retrieve_soil_conversion_table
retrieve_landuse_conversion_table
RasterExtraction
UUID
