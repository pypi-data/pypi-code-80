# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 16:40:16 2021

@author: chris.kerklaan


ThreediRasterGroup class checks for 3Di properties, alignment etc.

Input:
    1. Raster dictionary with standardized names
    2. Optional panden

Checks:
    1. Check alignemnt --> ALready included in rastergroups
    2. Check 3Di properties  --> Done!

Functions
    1. Convert input based on csv conversion tables
    2. Create based interception raster from panden

TODO:

Notes:
    1. Memory loading speeds up raster analysis, however is costly in memory
       Not all rasters are loaded into memory, e.g., it is not usefull to load
       a dem into memory since it is not used in conversion.
    2. Maximum memory is three rasters with 500.000.000 pixels each.
    3.

Ideas:
    1. Rasterfixer




"""
# First-party imports
import csv
import shutil
import pathlib
import logging
from pathlib import Path

# Third-party imports
import numpy as np
from osgeo import gdal

try:
    from numba import njit

    NUMBA_EXISTS = True
except ImportError:
    NUMBA_EXISTS = False

# local imports
from threedi_raster_edits.gis.rastergroup import RasterGroup
from threedi_raster_edits.gis.raster import Raster
from threedi_raster_edits.gis.vector import Vector
from threedi_raster_edits.utils.project import Progress

# GLOBALS
# Logger
logger = logging.getLogger(__name__)

# CSV path
FILE_PATH = str(pathlib.Path(__file__).parent.absolute()) + "/data/"
CSV_LANDUSE_PATH = FILE_PATH + "Conversietabel_landgebruik_2020.csv"
CSV_SOIL_PATH = FILE_PATH + "Conversietabel_bodem.csv"


class ThreediRasterGroup(RasterGroup):
    def __init__(
        self,
        dem_file: str,
        landuse_file: str = None,
        soil_file: str = None,
        interception_file: str = None,
        frict_coef_file: str = None,
        infiltration_file: str = None,
        initial_waterlevel_file: str = None,
        buildings: Vector = None,
        epsg=28992,
        nodata_value=-9999,
        data_type=gdal.GDT_Float32,
        np_data_type="f4",
    ):

        rasters = [Raster(dem_file, name="dem")]
        self.original_names = {"dem": Path(dem_file).stem}

        if landuse_file:
            logger.info("Loading landuse")
            landuse = Raster(landuse_file, name="landuse")
            landuse.load_to_memory()
            rasters.append(landuse)
            self.original_names["landuse"] = Path(landuse_file).stem

        if soil_file:
            logger.info("Loading soil")
            soil = Raster(soil_file, name="soil")
            soil.load_to_memory()
            rasters.append(soil)
            self.original_names["soil"] = Path(soil_file).stem

        if interception_file:
            logger.info("Loading interception")
            interception = Raster(interception_file, name="interception")
            rasters.append(interception)
            self.original_names["interception"] = Path(interception_file).stem

        if frict_coef_file:
            logger.info("Loading friction")
            friction = Raster(frict_coef_file, name="friction")
            rasters.append(friction)
            self.original_names["friction"] = Path(frict_coef_file).stem

        if infiltration_file:
            logger.info("Loading infiltration")
            infiltration = Raster(infiltration_file, name="infiltration")
            rasters.append(infiltration)
            self.original_names["infiltration"] = Path(infiltration_file).stem

        if initial_waterlevel_file:
            logger.info("Loading initial waterlevel")
            ini_wl = Raster(initial_waterlevel_file, name="initial_waterlevel")
            rasters.append(ini_wl)
            self.original_names["initial_waterlevel"] = Path(
                initial_waterlevel_file
            ).stem

        RasterGroup.__init__(self, rasters)

        if buildings:
            logger.debug("Setting buildings")
            self.buildings = buildings

        self.epsg = epsg
        self.data_type = data_type
        self.no_data_type = np_data_type
        self.nodata_value = nodata_value

        self.retrieve_soil_conversion_table = retrieve_soil_conversion_table
        self.retrieve_landuse_conversion_table = retrieve_landuse_conversion_table
        self.use_numba = NUMBA_EXISTS

    def check_table(self, table="soil"):
        logger.info("Checking tables")
        if table == "soil":
            if not hasattr(self, "ct_soil"):
                raise AttributeError(
                    """
                                     Please load soil csv using
                                     'load_soil_conversion_table'"""
                )
        elif table == "landuse":
            if not hasattr(self, "ct_lu"):
                raise AttributeError(
                    """
                                     Please load landuse csv using
                                     'load_landuse_conversion_table'"""
                )

    def check_properties(self):
        logger.info("Checking properties")
        return check_properties(
            self.rasters,
            nodata=self.nodata,
            projection=self.epsg,
            data_type=self.data_type,
        )

    def null_raster(self):
        logger.info("Creating null raster")
        copy = self.dem.empty_copy()
        null_array = np.zeros((int(copy.rows), int(copy.columns)))
        null_array[~self.dem.mask] = np.nan
        copy.array = null_array
        return copy

    def load_soil_conversion_table(self, csv_soil_path=CSV_SOIL_PATH):
        logger.info("Loading soil conversion table")
        self.ct_soil, self.ct_soil_info = load_csv_file(csv_soil_path, "soil")

    def load_landuse_conversion_table(self, csv_lu_path=CSV_LANDUSE_PATH):
        logger.info("Loading landuse conversion table")
        self.ct_lu, self.ct_lu_info = load_csv_file(csv_lu_path, "landuse")

    def generate_friction(self):
        logger.info("Generating friction")
        self.friction = classify(self.landuse, "Friction", self.ct_lu, self.use_numba)
        self.rasters.append(self.friction)

    def generate_permeability(self):
        logger.info("Generating permeability")
        self.permeability = classify(
            self.landuse, "Permeability", self.ct_lu, self.use_numba
        )
        self.rasters.append(self.permeability)

    def generate_interception(self):
        logger.info("Generating interception")
        self.interception = classify(
            self.landuse, "Interception", self.ct_lu, self.use_numba
        )
        self.rasters.append(self.interception)

    def generate_crop_type(self):
        logger.info("Generating crop type")
        self.crop_type = classify(self.landuse, "Crop_type", self.ct_lu, self.use_numba)
        self.rasters.append(self.crop_type)

    def generate_max_infiltration(self):
        logger.info("Generating max infiltration")
        self.max_infiltration = classify(
            self.soil, "Max_infiltration_rate", self.ct_soil, self.use_numba
        )
        self.rasters.append(self.max_infiltration)

    def generate_infiltration(self):
        logger.info("Generating infiltration")
        self.generate_permeability()
        self.generate_max_infiltration()

        output = self.dem.copy(shell=True)
        pbar = Progress(output.__len__(), "Generating infiltration")
        for perm_tile, inf_tile in zip(self.permeability, self.max_infiltration):
            perm_array = perm_tile.array
            inf_array = inf_tile.array

            infiltration_array = np.where(
                np.logical_and(
                    perm_array != self.nodata_value,
                    inf_array != self.nodata_value,
                ),
                perm_array * inf_array,
                self.nodata_value,
            ).astype(self.np_data_type)
            output.array = infiltration_array, *perm_tile.location
            pbar.update(quiet=False)

        self.infiltration = output
        self.infiltration.name = "Infiltration"
        self.rasters.append(self.infiltration)

    def generate_hydraulic_conductivity(self):
        logger.info("Generating hydraulic conductivity")
        self.hydraulic_conductivity = classify(
            self.soil, "Hydraulic_conductivity", self.ct_soil, self.use_numba
        )
        self.rasters.append(self.hydraulic_conductivity)

    def generate_building_interception(self, value):
        logger.info("Generating building interception")
        null = self.null_raster()
        value_raster = null.push_vector(self.buildings, value=value)
        self.interception = value_raster.align(
            self.dem, nodata_align=True, fill_value=0
        )
        self.interception.name = "Interception"
        self.rasters.append(self.interception)


def retrieve_soil_conversion_table(output_path):
    logger.info("retrieving soil conversion table")
    shutil.copyfile(CSV_SOIL_PATH, output_path)


def retrieve_landuse_conversion_table(output_path):
    logger.info("retrieving landuse conversion table")
    shutil.copyfile(CSV_LANDUSE_PATH, output_path)


def check_properties(
    raster_list,
    nodata=-9999,
    projection=28992,
    max_pixel_allow=1000000000,
    data_type=gdal.GDT_Float32,
    unit="metre",
    min_allow=-1000,
    max_allow=1000,
):
    # Has the raster the nodata value of -9999?
    output = {
        "nodata": {},
        "unit": {},
        "projection": {},
        "data_type": {},
        "resolution": {},
        "square_pixels": {},
        "min_max": {},
        "total_pixels": 0,
        "errors": [],
    }

    total_pixels = 0
    for raster in raster_list:

        # nodata value check
        if raster.nodata_value != nodata:
            msg = f"{raster.name} has a nodata value of {raster.nodata_value}"
            logger.debug(msg)
            output["errors"].append(("nodata_value", msg))
        output["nodata"][raster.name] = raster.nodata_value

        # unit check
        if raster.spatial_reference.unit != unit:
            msg = f"{raster.name} has not unit {unit}"
            logger.debug(msg)
            output["errors"].append(("unit", msg))
        output["unit"][raster.name] = raster.spatial_reference.unit

        # projection check
        if raster.spatial_reference.epsg != projection:
            msg = f"{raster.name} has not epsg {projection}"
            logger.debug(msg)
            output["errors"].append(("projection", msg))
        output["projection"][raster.name] = raster.spatial_reference.epsg

        # data type checl
        if raster.data_type != data_type:
            msg = f"{raster.name} is not a {gdal.GetDataTypeName(data_type)}"
            logger.debug(msg)
            output["errors"].append(("data_type", msg))
        output["data_type"][raster.name] = gdal.GetDataTypeName(data_type)

        # square pixel check
        if abs(raster.resolution["width"]) != abs(raster.resolution["height"]):
            msg = f"{raster.name} has not a square pixel"
            output["errors"].append(("width/height", msg))
        output["square_pixels"][raster.name] = raster.resolution

        # extreme value check
        _max, _min = np.nanmax(raster.array), np.nanmin(raster.array)
        if not (min_allow < _max < max_allow and min_allow < _min < max_allow):
            msg = f"{raster.name} has extreme values < {min_allow}, > {max_allow} "
            logger.debug(msg)
            output["errors"].append(("extreme_values", msg))
        output["min_max"][raster.name] = {"min": _min, "max": _max}

        total_pixels += raster.pixels

    # max pixel allowed check
    if total_pixels > max_pixel_allow:
        msg = f"Rasters combined pixels are larger than {max_pixel_allow}"
        logger.debug(msg)
        output["errors"].append(("maximum_allowed_pixels", msg))

    output["total_pixels"] = total_pixels

    if len(output["errors"]) == 0:
        logger.debug("ThreediRasterGroup - Check properties found no problems")
    return output


def load_csv_file(csv_path, csv_type="landuse"):
    csv_data = {}
    csv_info = {}
    if csv_type == "landuse":
        csv_structure = {
            1: "description",
            2: "unit",
            3: "range",
            4: "type",
        }
        meta_list = [1, 2, 3, 4]
    elif csv_type == "soil":
        csv_structure = {
            1: "description",
            2: "source",
            3: "unit",
            4: "range",
            5: "type",
        }
        meta_list = [1, 2, 3, 4, 5]

    with open(csv_path) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=";")
        for i, line in enumerate(csv_reader):

            # headers
            if i == 0:
                headers = line
                for column_value in line:
                    csv_data[column_value] = []
                    csv_info[column_value] = {}

            # units, descriptions, ranges etc.
            elif i in meta_list:

                for column_index, column_value in enumerate(line):
                    field = csv_structure[i]
                    csv_info[headers[column_index]][field] = column_value
            # csv data
            else:
                for column_index, column_value in enumerate(line):
                    column = headers[column_index]
                    column_type = csv_info[column]["type"]

                    if column_value == "":
                        csv_data[column].append(None)
                    else:
                        if column_type == "Integer":
                            column_value = int(column_value)
                        elif column_type == "Double" or column_type == "Real":
                            column_value = float(column_value)
                        elif column_type == "String":
                            column_value = str(column_value)
                        csv_data[column].append(column_value)

        return csv_data, csv_info


def classify(raster: Raster, table: str, ct: dict, use_numba: bool):
    """input is a table to classify,
    raster is the template raster,
    ct is the conversion table
    returns a dictionary of classified rasters"""

    ct_codes = ct["Code"]
    ct_table = ct[table]
    pbar = Progress(raster.__len__(), "Classifying {}".format(table))

    output = raster.copy(shell=True)
    for tile in raster:
        array = tile.array

        if use_numba:
            output_array = nb_classify_array(array, ct_table[1:], ct_codes[1:])
        else:
            output_array = classify_array(array, ct_table, ct_codes)

        if type(output_array) == None:
            output.array = array, *tile.location
        else:
            output.array = output_array, *tile.location

        # # Delete array
        del array
        del output_array

        pbar.update(False)
    output.name = table
    return output


def classify_array(array, ct_table, ct_codes):
    if np.isnan(array).all():
        return

    codes = np.unique(array[~np.isnan(array)])
    output_array = np.copy(array)
    for code in codes:
        output_array[array == code] = ct_table[ct_codes.index(code)]

    return output_array


if NUMBA_EXISTS:

    @njit()
    def nb_classify_array(array, ct_table, ct_codes):
        """ about 2 times faster"""
        if np.isnan(array).all():
            return
        m, n = array.shape
        output_array = np.copy(array)
        for i in range(m):
            for j in range(n):
                value = array[i, j]

                if np.isnan(value):
                    continue

                output_array[i, j] = ct_table[ct_codes.index(value)]

        return output_array
