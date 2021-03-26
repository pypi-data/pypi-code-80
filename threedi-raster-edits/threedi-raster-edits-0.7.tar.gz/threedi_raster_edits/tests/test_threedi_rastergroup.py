# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 09:35:28 2021

@author: chris.kerklaan

#TODO functions:
    1. Memory counter
    
Currently supported functions
    1. Check properties
        1. nodata
        2. projection
        3. data_type
        4. extreme_values
        5. max_allowed_pixels --> takes a long time, so currently switched off
        6. Not square pixels --> could not create this hence not present
    2. Check null rasters 
    3. Check load csv
    4. Checks generate functions
        1. Friction
        2. Interceptions
        3. Infiltration (Permeability and max infiltration)
        4. Crop type
        5. Hydrauilic conductivty
        6. Building interception
        
"""
# First-party imports
import pathlib

# Third-party imports
import numpy as np
from osgeo import gdal

# Local imports
from threedi_raster_edits.threedi.rastergroup import ThreediRasterGroup
from threedi_raster_edits.gis.raster import Raster
from threedi_raster_edits.gis.vector import Vector

# Globals
# TEST_DIRECTORY = "//utr-3fs-01.nens.local/WorkDir/C_Kerklaan/scripts/base/tests/input/threedi_raster_group/"
TEST_DIRECTORY = (
    str(pathlib.Path(__file__).parent.absolute()) + "/data/threedi_raster_group/"
)

MANDATORY_TITLES_SOIL = [
    "Title",
    "Code",
    "Soiltype",
    "Max_infiltration_rate",
    "Hydraulic_conductivity",
]
MANDATORY_TITLES_LANDUSE = [
    "Code",
    "Landuse",
    "Friction",
    "Permeability",
    "Interception",
    "Crop_type",
]


table_path = TEST_DIRECTORY + "conversietabellen/"
csv_landuse_file = table_path + "Conversietabel_landgebruik_2020.csv"
csv_soil_file = table_path + "Conversietabel_bodem.csv"
dem_file = TEST_DIRECTORY + "dem.tif"
interception_file = TEST_DIRECTORY + "interception.tif"
frict_coef_file = TEST_DIRECTORY + "friction.tif"
infiltration_file = TEST_DIRECTORY + "infiltration.tif"
soil_file = TEST_DIRECTORY + "soil.tif"
landuse_file = TEST_DIRECTORY + "landuse.tif"
crop_type_file = TEST_DIRECTORY + "crop_type.tif"
hydraulic_conductivity_file = TEST_DIRECTORY + "hydraulic_conductivity.tif"
buildings_path = TEST_DIRECTORY + "buildings.shp"
building_interception_file = TEST_DIRECTORY + "building_interception.tif"


def test_check_nodata_properties():
    """ tests if checks work for nodata value equals -9999"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        interception_file=interception_file,
        frict_coef_file=frict_coef_file,
        infiltration_file=infiltration_file,
    )
    group.dem.nodata_value = -8888
    checks = group.check_properties()

    assert len(checks["errors"]) > 0

    if len(checks["errors"]) > 0:
        assert checks["errors"][0][0] == "nodata_value"


def test_check_projection_properties():
    """ tests if checks work for projection and units if it is 28992 and metere"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        interception_file=interception_file,
        frict_coef_file=frict_coef_file,
        infiltration_file=infiltration_file,
    )

    group.dem.spatial_reference = 4326
    checks = group.check_properties()

    errors_present = len(checks["errors"]) > 0
    assert errors_present
    if errors_present:
        assert checks["errors"][0][0] == "unit"
        assert checks["errors"][1][0] == "projection"


def test_check_data_type_properties():
    """ tests if checks work for data_type"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        interception_file=interception_file,
        frict_coef_file=frict_coef_file,
        infiltration_file=infiltration_file,
    )
    group.insert(group.dem.empty_copy(data_type=gdal.GDT_Int16))

    checks = group.check_properties()

    errors_present = len(checks["errors"]) > 0
    assert errors_present

    if errors_present:
        assert checks["errors"][0][0] == "data_type"


def test_check_extreme_values_properties():
    """ tests if checks work for extreme values"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        interception_file=interception_file,
        frict_coef_file=frict_coef_file,
        infiltration_file=infiltration_file,
    )
    group.dem.load_to_memory()
    group.dem.array = group.dem.array + 1 * 10 ** 8
    checks = group.check_properties()

    errors_present = len(checks["errors"]) > 0
    assert errors_present

    if errors_present:
        assert checks["errors"][0][0] == "extreme_values"


def test_check_max_allowed_pixels_properties():
    """ tests if checks work for maximum allowed pixels by making an empty copy"""
    group = ThreediRasterGroup(dem_file=dem_file)
    copy = group.dem.empty_copy(100000, 10001)
    group["dem"] = copy
    checks = group.check_properties()
    errors_present = len(checks["errors"]) > 0
    assert errors_present
    assert checks["errors"][0][0] == "maximum_allowed_pixels"
    group = None


def test_null_rasters():
    """ tests null rasters"""
    group = ThreediRasterGroup(dem_file=dem_file)
    array = group.null_raster().array
    assert np.nansum(array) == 0.0


def test_load_csv_soil():
    """ tests load csv on keys, values and if exists in object"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        landuse_file=landuse_file,
        soil_file=soil_file,
    )

    group.load_soil_conversion_table(csv_soil_file)
    assert hasattr(group, "ct_soil")
    if hasattr(group, "ct_soil"):
        for title in MANDATORY_TITLES_SOIL:
            assert title in group.ct_soil.keys()
            values = group.ct_soil[title]
            assert len(values) > 0


def test_load_csv_lu():
    """ tests load csv on keys, values and if exists in object"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        landuse_file=landuse_file,
        soil_file=soil_file,
    )

    group.load_landuse_conversion_table(csv_landuse_file)
    assert hasattr(group, "ct_lu")

    if hasattr(group, "ct_lu"):
        for title in MANDATORY_TITLES_LANDUSE:
            assert title in group.ct_lu.keys()

            values = group.ct_lu[title]
            assert len(values) > 0


def test_generate_friction():
    """ tests if generated friction using total counts"""

    group = ThreediRasterGroup(dem_file=dem_file, landuse_file=landuse_file)

    group.load_landuse_conversion_table(csv_landuse_file)
    group.generate_friction()
    or_sum = np.nansum(Raster(frict_coef_file).array)
    generated_sum = np.nansum(group.friction.array)
    assert or_sum == generated_sum


def test_generate_interception():
    """ tests if generated interceptions using total counts"""

    group = ThreediRasterGroup(dem_file=dem_file, landuse_file=landuse_file)

    group.load_landuse_conversion_table(csv_landuse_file)
    group.generate_interception()

    or_sum = np.nansum(Raster(interception_file).array)
    generated_sum = np.nansum(group.interception.array)
    assert or_sum == generated_sum


def test_generate_infiltration():
    """ tests if generated infiltraion using total counts"""

    group = ThreediRasterGroup(
        dem_file=dem_file,
        landuse_file=landuse_file,
        soil_file=soil_file,
    )

    group.load_landuse_conversion_table(csv_landuse_file)
    group.load_soil_conversion_table(csv_soil_file)
    group.generate_infiltration()

    or_sum = np.nansum(Raster(infiltration_file).array)
    generated_sum = np.nansum(group.infiltration.array)
    assert or_sum == generated_sum


def test_generate_crop_type():
    """ tests if generated crop type using total counts"""

    group = ThreediRasterGroup(dem_file=dem_file, landuse_file=landuse_file)

    group.load_landuse_conversion_table(csv_landuse_file)
    group.generate_crop_type()

    or_sum = np.nansum(Raster(crop_type_file).array)
    generated_sum = np.nansum(group.crop_type.array)
    assert or_sum == generated_sum


def test_generate_hydraulic_conductivity():
    """ tests if generated hydraulic conductivity using total counts"""

    group = ThreediRasterGroup(dem_file=dem_file, soil_file=soil_file)

    group.load_soil_conversion_table(csv_soil_file)
    group.generate_hydraulic_conductivity()
    or_sum = np.nansum(Raster(hydraulic_conductivity_file).array)
    generated_sum = np.nansum(group.hydraulic_conductivity.array)
    assert or_sum == generated_sum


def test_generate_building_interception():
    """ tests if generated buildings interception using total counts"""

    group = ThreediRasterGroup(dem_file, buildings=Vector(buildings_path))
    group.generate_building_interception(10)
    group.interception.write(TEST_DIRECTORY + "building_interception2.tif")
    or_sum = np.nansum(Raster(building_interception_file).array)
    generated_sum = np.nansum(group.interception.array)
    assert or_sum == generated_sum


# def test_memory_capacity():
#     """ rastergroup should be able to handle three rasters of 500.000.000
#         pixels each
#     """
#     group = ThreediRasterGroup(dem_file=dem_file,
#                                 landuse_file=landuse_file,
#                                 soil_file=soil_file)
#     copy = group.dem.empty_copy(20000, 25000)
#     group["dem"] = copy

#     landuse = copy.empty_copy()
#     for tile in copy:
#         array = tile.array
#         array[array==0]=1
#         landuse.array = array, *tile.location
#     landuse.name ="landuse"

#     group["landuse"] = landuse

#     soil = copy.empty_copy()
#     for tile in copy:
#         array = tile.array
#         array[array==0]=1
#         soil.array = array, *tile.location
#     soil.name = "soil"
#     group["soil"] = soil


#     group.load_landuse_conversion_table(csv_landuse_file)
#     group.load_soil_conversion_table(csv_soil_file)

#     group.generate_friction()
#     group.generate_permeability()
#     group.generate_interception()
#     group.generate_crop_type()
#     group.generate_max_infiltration()
#     group.generate_infiltration()
#     group.generate_hydraulic_conductivity()

#     assert True
