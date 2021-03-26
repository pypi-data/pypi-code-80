# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Filename: core.py
#  Purpose: module to interact with the NLLoc
#   Author: uquake development team
#    Email: devs@uquake.org
#
# Copyright (C) 2016 uquake development team
# --------------------------------------------------------------------
"""
module to interact with the NLLoc

:copyright:
    uquake development team (devs@uquake.org)
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""

import os
import shutil
import tempfile
from datetime import datetime
from glob import glob
from struct import unpack
from time import time
import numpy as np

from obspy import UTCDateTime
from ..core.inventory import Inventory, read_inventory
from ..core.logging import logger
from ..grid.base import read_grid
from ..core.event import (Arrival, Catalog, Origin, Event, AttribDict)

import pickle

from ..grid import nlloc as grid

from uuid import uuid4
from pathlib import Path


def validate(value, choices):
    if value not in choices:
        msg = f'value should be one of the following choices\n:'
        for choice in choices:
            msg += f'{choice}\n'
        raise ValueError(msg)
    return True


def validate_type(obj, expected_type):
    if type(obj) is not expected_type:
        raise TypeError('object is not the right type')


__valid_geographic_transformation__ = ['GLOBAL', 'SIMPLE', 'NONE', 'SDC',
                                       'LAMBERT']

__valid_reference_ellipsoid__ = ['WGS-84', 'GRS-80', 'WGS-72', 'Australian',
                                 'Krasovsky', 'International', 'Hayford-1909'
                                 'Clarke-1880', 'Clarke-1866', 'Airy Bessel',
                                 'Hayford-1830', 'Sphere']

__valid_units__ =['METER', 'KILOMETER']


class Grid2Time:
    def __init__(self, srces, grid_transform, base_directory, base_name,
                 verbosity=1, random_seed=1000, p_wave=True, s_wave=True,
                 calculate_angles=True, model_directory='models',
                 grid_directory='grids'):
        """
        Build the control file and run the Grid2Time program.

        Note that at this time the class does not support any geographic
        transformation

        :param srces: inventory data
        :type srces: Srces
        :param base_directory: the base directory of the project
        :type base_directory: str
        :param base_name: the network code
        :type base_name: str
        :param verbosity: sets the verbosity level for messages printed to
        the terminal ( -1 = completely silent, 0 = error messages only,
        1 = 0 + higher-level warning and progress messages,
        2 and higher = 1 + lower-level warning and progress messages +
        information messages, ...) default: 1
        :type verbosity: int
        :param random_seed:  integer seed value for generating random number
        sequences (used by program NLLoc to generate Metropolis samples and
        by program Time2EQ to generate noisy time picks)
        :param p_wave: if True calculate the grids for the P-wave
        :type p_wave: bool
        :param s_wave: if True calculate the grids for the S-wave
        :type s_wave: bool
        :param calculate_angles: if true calculate the azimuth and the
        take-off angles
        :type calculate_angles: bool
        :param model_directory: location of the model directory relative to
        the base_directory
        :type model_directory: str
        :param grid_directory: location of the grid directory relative to
        the base_directory
        """

        self.verbosity = verbosity
        self.random_seed = random_seed
        self.base_name = base_name

        self.base_directory = Path(base_directory)
        self.velocity_model_path = self.base_directory / f'{model_directory}'
        self.grid_path = self.base_directory / f'{grid_directory}'

        # create the velocity_model_path and the grid_path if they do not exist
        self.grid_path.mkdir(parents=True, exist_ok=True)
        self.velocity_model_path.mkdir(parents=True, exist_ok=True)

        self.calculate_p_wave = p_wave
        self.calculate_s_wave = s_wave
        self.calculate_angles = calculate_angles

        if type(inventory) is not Inventory:
            raise TypeError('inventory must be '
                            '"uquake.core.inventory.Inventory" type')
        self.inventory = inventory

    def run(self):
        if self.calculate_p_wave:
            self.__write_control_file__('P')
            # run

        if self.calculate_s_wave:
            self.__write_control_file__('S')

    def __write_control_file__(self, phase):

        ctrl_dir = f'{self.base_directory}/run/'
        Path(ctrl_dir).mkdir(parents=True, exist_ok=True)

        # create the directory if the directory does not exist

        ctrl_file = ctrl_dir + f'{str(uuid4())}.ctl'
        with open(ctrl_file, 'w') as ctrl:
            # writing the control section
            ctrl.write(f'CONTROL {self.verbosity} {self.random_seed}\n')

            # writing the geographic transformation section
            ctrl.write('TRANS NONE\n')

            # writing the Grid2Time section
            out_line = f'GTFILES ' \
                       f'{self.velocity_model_path}/{self.base_name} ' \
                       f'{self.grid_path}/{self.base_name} ' \
                       f'{phase} 0\n'

            ctrl.write(out_line)

            if self.calculate_angles:
                angle_mode = 'ANGLES_YES'
            else:
                angle_mode = 'ANGLE_NO'

            ctrl.write(f'GTMODE GRID3D {angle_mode}\n')

            for sensor in self.inventory.sensors:
                # test if sensor name is shorter than 6 characters

                out_line = f'GTSRCE {sensor.code} XYZ ' \
                           f'{sensor.x / 1000:>10.6f} ' \
                           f'{sensor.y / 1000 :>10.6f} ' \
                           f'{sensor.z / 1000 :>10.6f} ' \
                           f'0.00\n'

                ctrl.write(out_line)

            ctrl.write(f'GT_PLFD 1.0e-4 {self.verbosity + 1}\n')


class Control:
    def __init__(self, message_flag=-1, random_seed=1000):
        """
        Control section
        :param message_flag: (integer, min:-1, default:1) sets the verbosity
        level for messages printed to the terminal ( -1 = completely silent,
        0 = error messages only, 1 = 0 + higher-level warning and progress
        messages, 2 and higher = 1 + lower-level warning and progress
        messages + information messages, ...)
        :param random_seed:(integer) integer seed value for generating random
        number sequences (used by program NLLoc to generate Metropolis samples
        and by program Time2EQ to generate noisy time picks)
        """
        try:
            self.message_flag=int(message_flag)
        except Exception as e:
            raise e

        try:
            self.random_seed=int(random_seed)
        except Exception as e:
            raise e

    def __repr__(self):
        return f'CONTROL {self.message_flag} {self.random_seed}'


class GeographicTransformation:
    type = 'GeographicTransformation'

    def __init__(self, transformation='NONE'):
        validate(transformation, __valid_geographic_transformation__)
        self.transformation = transformation

    def __repr__(self):
        line = f'TRANS {self.transformation}'
        return line


class SimpleSDCGeographicTransformation(GeographicTransformation):

    def __init__(self, latitude_origin, longitude_origin,
                 rotation_angle, simple=True):
        """
        The SIMPLE or SDC transformation only corrects longitudinal
        distances as a function of latitude Algorithm:

        >> x = (long - longOrig) * 111.111 * cos(lat_radians);
        >> y = (lat - latOrig) * 111.111;
        >> lat = latOrig + y / 111.111;
        >> long = longOrig + x / (111.111 * cos(lat_radians));

        :param latitude_origin: (float, min:-90.0, max:90.0) latitude in
        decimal degrees of the rectangular coordinates origin
        :param longitude_origin: (float, min:-180.0, max:180.0) longitude in
        decimal degrees of the rectangular coordinates origin
        :param rotation_angle: (float, min:-360.0, max:360.0) rotation angle
        of geographic north in degrees clockwise relative to the rectangular
        coordinates system Y-axis
        :param simple: Transformation is set to SIMPLE if simple is True.
        Transformation is set to SDC if simple is set to False
        """

        if -90 > latitude_origin > 90:
            raise ValueError('latitude_origin must be comprised between '
                             '-90 and 90 degrees')
        if -180 > longitude_origin > 180:
            raise ValueError('longitude_origin must be comprised between '
                             '-180 and 180 degrees')

        if -360 > rotation_angle > 360:
            raise ValueError('the rotation angle must be comprised between '
                             '-360 and 360 degrees')

        self.latitude_origin = latitude_origin
        self.longitude_origin = longitude_origin
        self.rotation_angle = rotation_angle

        if simple:
            transformation = 'SIMPLE'
        else:
            transformation = 'SDC'

        super.__init__(transformation=transformation)

    def __setattr__(self, key, value):
        if key in self.__dict__.keys():
            self.__dict__[key] = value

    def __repr__(self):
        line = f'TRANS {self.transformation} {self.latitude_origin} ' \
               f'{self.longitude_origin} {self.rotation_angle}'

        return line


class LambertGeographicTransformation(GeographicTransformation):
    def __init__(self, reference_ellipsoid, latitude_origin,
                 longitude_origin, first_standard_parallax,
                 second_standard_parallax, rotation_angle):
        """
        Define a Lambert coordinates system for transformation from Lambert
        geographic coordinates to a cartesian/rectangular system.
        :param reference_ellipsoid: (choice: WGS-84 GRS-80 WGS-72
        Australian Krasovsky International Hayford-1909 Clarke-1880
        Clarke-1866 Airy Bessel Hayford-1830 Sphere) reference ellipsoid name
        :param latitude_origin: (float, min:-90.0, max:90.0) latitude in
        decimal degrees of the rectangular coordinates origin
        :param longitude_origin: (float, min:-180.0, max:180.0) longitude in
        decimal degrees of the rectangular coordinates origin
        :param first_standard_parallax: (float, min:-90.0, max:90.0) first
        standard parallels (meridians) in decimal degrees
        :param second_standard_parallax: (float, min:-90.0, max:90.0)
        second standard parallels (meridians) in decimal degrees
        :param rotation_angle: (float, min:-360.0, max:360.0) rotation angle
        of geographic north in degrees clockwise relative to the rectangular
        coordinates system Y-axis
        """

        validate(reference_ellipsoid, __valid_reference_ellipsoid__)

        self.reference_ellipsoid = reference_ellipsoid

        if -90 > latitude_origin > 90:
            raise ValueError('latitude_origin must be comprised between '
                             '-90 and 90 degrees')
        if -180 > longitude_origin > 180:
            raise ValueError('longitude_origin must be comprised between '
                             '-180 and 180 degrees')

        if -360 > rotation_angle > 360:
            raise ValueError('the rotation angle must be comprised between '
                             '-360 and 360 degrees')

        if -90 > first_standard_parallax > 90:
            raise ValueError('first_standard_parallax must be comprised '
                             'between -90 and 90 degrees')

        if -90 > second_standard_parallax > 90:
            raise ValueError('second_standard_parallax must be comprised '
                             'between -90 and 90 degrees')

        self.latitude_origin = latitude_origin
        self.longitude_origin = longitude_origin
        self.rotation_angle = rotation_angle
        self.first_standard_parallax = first_standard_parallax
        self.second_standard_parallax = second_standard_parallax

    def __repr__(self):
        line = f'TRANS LAMBERT {self.reference_ellipsoid} ' \
               f'{self.latitude_origin} {self.longitude_origin} ' \
               f'{self.first_standard_parallax} ' \
               f'{self.second_standard_parallax} {self.rotation_angle}'


class LocSearchGrid:
    def __init__(self, num_sample_draw=1000):
        """

        :param num_sample_draw: specifies the number of scatter samples to
        draw from each saved PDF grid ( i.e. grid with gridType = PROB_DENSITY
        and saveFlag = SAVE ) No samples are drawn if saveFlag < 0.
        :type num_sample_draw: int
        """
        self.num_sample_draw = num_sample_draw

    def __repr__(self):
        return f'GRID {self.num_sample_draw}\n'

    @property
    def type(self):
        return 'LOCSEARCH'


class LocSearchMetropolis:
    def __init__(self, num_samples, num_learn, num_equil, num_begin_save,
                 num_skip, step_init, step_min, prob_min, step_fact=8.):
        """
        Container for the Metropolis Location algorithm parameters

        The Metropolis-Gibbs algorithm performs a directed random walk within
        a spatial, x,y,z volume to obtain a set of samples that follow the
        3D PDF for the earthquake location. The samples give and estimate of
        the optimal hypocenter and an image of the posterior probability
        density function (PDF) for hypocenter location.

        Advantages:

        1. Does not require partial derivatives, thus can be used with
        complicated, 3D velocity structures
        2. Accurate recovery of moderately irregular (non-ellipsoidal)
        PDF's with a single minimum
        3. Only only moderately slower (about 10 times slower) than linearised,
        iterative location techniques, and is much faster
        (about 100 times faster) than the grid-search
        4. Results can be used to obtain confidence contours

        Drawbacks:

        1. Stochastic coverage of search region - may miss important features
        2. Inconsistent recovery of very irregular (non-ellipsoidal)
        PDF's with multiple minima
        3. Requires careful selection of sampling parameters
        4. Attempts to read full 3D travel-time grid files into memory,
        thus may run very slowly with large number of observations and large
        3D travel-time grids

        :param num_samples: total number of accepted samples to obtain (min:0)
        :type num_samples: int
        :param num_learn: number of accepted samples for learning stage of
        search (min:0)
        :type num_learn: int
        :param num_equil: number of accepted samples for equilibration stage
        of search (min:0)
        :type num_equil: int
        :param num_begin_save: number of accepted samples after which to begin
        saving stage of search, denotes end of equilibration stage (min:0)
        :type num_begin_save: int
        :param num_skip: number of accepted samples to skip between saves
        (numSkip = 1 saves every accepted sample, min:1)
        :type num_skip: int
        :param step_init: initial step size in km for the learning stage
        (stepInit < 0.0 gives automatic step size selection. If the search
        takes too long, the initial step size may be too large;
        this may be the case if the search region is very large relative
        to the volume of the high confidence region for the locations.)
        :type step_init: float
        :param step_min: minimum step size allowed during any search stage
        (This parameter should not be critical, set it to a low value. min:0)
        :type step_min: float
        :param prob_min: minimum value of the maximum probability (likelihood)
        that must be found by the end of learning stage, if this value is not
        reached the search is aborted (This parameters allows the filtering of
        locations outside of the search grid and locations with large
        residuals.)
        :type prob_min: float
        :param step_fact: step factor for scaling step size during
        equilibration stage (Try a value of 8.0 to start.) Default=8.
        :type step_fact: float
        """

        self.num_samples = num_samples
        self.num_learn = num_learn
        self.num_equil = num_equil
        self.num_begin_save = num_begin_save
        self.num_skip = num_skip
        self.step_init = step_init
        self.step_min = step_min
        self.prob_min = prob_min
        self.step_fact = step_fact

    def __repr__(self):
        line = f'LOCSEARCH MET {self.num_samples} {self.num_learn} ' \
               f'{self.num_equil} {self.num_begin_save} {self.num_skip} ' \
               f'{self.step_min} {self.step_min} {self.step_fact} ' \
               f'{self.prob_min}\n'

        return line

    @classmethod
    def init_with_default(cls):
        pass

    @property
    def type(self):
        return 'LOCSEARCH'


class LocSearchOctTree:
    def __init__(self, init_num_cell_x, init_num_cell_y, init_num_cell_z,
                 min_node_size, max_num_nodes, num_scatter,
                 use_station_density=False, stop_on_min_node_size=True):
        """
        Container for the Octree Location algorithm parameters

        Documenation: http://alomax.free.fr/nlloc/octtree/OctTree.html

        Developed in collaboration with Andrew Curtis; Schlumberger Cambridge
        Research, Cambridge CB3 0EL, England; curtis@cambridge.scr.slb.com

        The oct-tree importance sampling algorithm gives accurate, efficient
        and complete mapping of earthquake location PDFs in 3D space (x-y-z).

        Advantages:

        1. Much faster than grid-search (factor 1/100)
        2. More global and complete than Metropolis-simulated annealing
        3. Simple, with very few parameters (initial grid size, number of samples)

        Drawbacks:

        1. Results are weakly dependant on initial grid size - the method may
        not identify narrow, local maxima in the PDF.
        2. Attempts to read full 3D travel-time grid files into memory,
        thus may run very slowly with large number of observations and large
        3D travel-time grids

        :param init_num_cell_x: initial number of octtree cells in the x
        direction
        :type init_num_cell_x: int
        :param init_num_cell_y: initial number of octtree cells in the y
        direction
        :type init_num_cell_y: int
        :param init_num_cell_z: initial number of octtree cells in the z
        direction
        :type init_num_cell_z: int
        :param min_node_size: smallest octtree node side length to process,
        the octree search is terminated after a node with a side smaller
        than this length is generated
        :type min_node_size: float
        :param max_num_nodes: total number of nodes to process
        :type max_num_nodes: int
        :param num_scatter: the number of scatter samples to draw from the
        octtree results
        :type num_scatter: int
        :param use_station_density: flag, if True weights oct-tree cell
        probability values used for subdivide decision in proportion to number
        of stations in oct-tree cell; gives higher search priority to cells
        containing stations, stablises convergence to local events when global
        search used with dense cluster of local stations
        (default:False)
        :type use_station_density: bool
        :param stop_on_min_node_size: flag, if True, stop search when first
        min_node_size reached, if False stop subdividing a given cell when
        min_node_size reached (default:True)
        :type stop_on_min_node_size: bool
        """

        self.init_num_cell_x = init_num_cell_x
        self.init_num_cell_y = init_num_cell_y
        self.init_num_cell_z = init_num_cell_z
        self.min_node_size = min_node_size
        self.max_num_nodes = max_num_nodes
        self.num_scatter = num_scatter
        self.use_station_density = use_station_density
        self.stop_on_min_node_size = stop_on_min_node_size

    @classmethod
    def init_default(cls):
        init_num_cell_x = 5
        init_num_cell_y = 5
        init_num_cell_z = 5
        min_node_size = 1E-6
        max_num_nodes = 5000
        num_scatter = 500
        use_station_density = False
        stop_on_min_node_size = True
        return cls(init_num_cell_x, init_num_cell_y, init_num_cell_z,
                   min_node_size, max_num_nodes, num_scatter,
                   use_station_density, stop_on_min_node_size)

    def __repr__(self):
        line = f'LOCSEARCH OCT {self.init_num_cell_x} ' \
               f'{self.init_num_cell_y} {self.init_num_cell_z} ' \
               f'{self.min_node_size} {self.max_num_nodes} ' \
               f'{self.num_scatter} {self.use_station_density:d} ' \
               f'{self.stop_on_min_node_size:d}\n'

        return line

    @property
    def type(self):
        return 'LOCSEARCH'


class GaussianModelErrors:
    def __init__(self, sigma_time, correlation_length):
        """
        container for Gaussian Error Model
        :param sigma_time: typical error in seconds for travel-time to one
        station due to model errors
        :type sigma_time: float
        :param correlation_length: correlation length that controls covariance
        between stations ( i.e. may be related to a characteristic scale length
        of the medium if variations on this scale are not included in the
        velocity model)
        :type correlation_length: float
        """

        self.sigma_time = sigma_time
        self.correlation_length = correlation_length

    @classmethod
    def init_default(cls):
        sigma_time = 1E-3
        correlation_length = 1E-3

        return cls(sigma_time, correlation_length)

    def __repr__(self):
        return f'LOCGAU {self.sigma_time} {self.correlation_length}\n'


__valid_location_methods__ = ['GAU_ANALYTIC', 'EDT', 'EDT_OT_WT',
                              'EDT_OT_WT_ML']


class LocationMethod:
    def __init__(self, method, max_dist_sta_grid, min_number_phases,
                 max_number_phases, min_number_s_phases, vp_vs_ratio,
                 max_number_3d_grid_memory, min_dist_sta_grid):
        """
        container for location method
        :param method: location method/algorithm ( GAU_ANALYTIC = the inversion
        approach of Tarantola and Valette (1982) with L2-RMS likelihood
        function. EDT = Equal Differential Time likelihood function cast into
        the inversion approach of Tarantola and Valette (1982) EDT_OT_WT =
        Weights EDT-sum probabilities by the variance of origin-time estimates
        over all pairs of readings. This reduces the probability (PDF values)
        at points with inconsistent OT estimates, and leads to more compact
        location PDF's. EDT_OT_WT_ML = version of EDT_OT_WT with EDT
        origin-time weighting applied using a grid-search, maximum-likelihood
        estimate of the origin time. Less efficient than EDT_OT_WT which
        uses simple statistical estimate of the origin time.)
        :param max_dist_sta_grid: maximum distance in km between a station and the
        center of the initial search grid; phases from stations beyond this
        distance will not be used for event location
        :param min_number_phases: minimum number of phases that must be
        accepted before event will be located
        :param max_number_phases: maximum number of accepted phases that will
        be used for event location; only the first maxNumberPhases read from
        the phase/observations file are used for location
        :param min_number_s_phases: minimum number of S phases that must be
        accepted before event will be located
        :param vp_vs_ratio: P velocity to S velocity ratio. If VpVsRatio > 0.0
        then only P phase travel-times grids are read and VpVsRatio is used to
        calculate S phase travel-times. If VpVsRatio < 0.0 then S phase
        travel-times grids are used.
        :param max_number_3d_grid_memory: maximum number of 3D travel-time
        grids to attempt to read into memory for Metropolis-Gibbs search. This
        helps to avoid time-consuming memory swapping that occurs if the total
        size of grids read exceeds the real memory of the computer. 3D grids
        not in memory are read directly from disk. If maxNum3DGridMemory < 0
        then NLLoc attempts to read all grids into memory.
        :param min_dist_sta_grid: minimum distance in km between a station and
        the center of the initial search grid; phases from stations closer than
        this distance will not be used for event location
        """

        validate(method, __valid_location_methods__)
        self.method = method

        self.max_dist_sta_grid = max_dist_sta_grid
        self.min_number_phases = min_number_phases
        self.max_number_phases = max_number_phases
        self.min_number_s_phases = min_number_s_phases
        self.vp_vs_ratio = vp_vs_ratio
        self.max_number_3d_grid_memory = max_number_3d_grid_memory
        self.min_dist_sta_grid = min_dist_sta_grid

    @classmethod
    def init_default(cls):
        method = 'EDT_OT_WT'
        max_dist_sta_grid = 9999.
        min_number_phases = 6
        max_number_phases = -1
        min_number_s_phases = -1
        vp_vs_ratio = -1
        max_number_3d_grid_memory = 0
        min_dist_sta_grid = 0

        return cls(method, max_dist_sta_grid, min_number_phases,
                   max_number_phases, min_number_s_phases, vp_vs_ratio,
                   max_number_3d_grid_memory, min_dist_sta_grid)

    def __repr__(self):
        line = f'LOCMETH {self.method} {self.max_dist_sta_grid:.1f} ' \
               f'{self.min_number_phases} {self.max_number_phases} ' \
               f'{self.min_number_s_phases} {self.vp_vs_ratio} ' \
               f'{self.max_number_3d_grid_memory}\n'

        return line


class Observations:
    def __init__(self, picks, p_pick_error=1e-3, s_pick_error=1e-3):
        """

        :param picks: a list of pick object
        :type picks: list of uquake.core.event.pick
        :param p_pick_error: p-wave picking error in second
        :param s_pick_error: s-wave picking error in second
        """

        self.picks = picks
        self.p_pick_error = p_pick_error
        self.s_pick_error = s_pick_error

    @classmethod
    def from_event(cls, event, p_pick_error=1e-3, s_pick_error=1e-3,
                   origin_index=None):

        if type(event) is Catalog:
            event = event[0]
            logger.warning('An object type Catalog was provided. Taking the '
                           'first event of the catalog. This may lead to '
                           'unwanted behaviour')

        if origin_index is None:
            if event.preferred_origin() is None:
                logger.warning('The preferred origin is not defined. The last'
                               'inserted origin will be use. This may lead '
                               'to unwanted behaviour')

                origin = event.origins[-1]
            else:
                origin = event.preferred_origin()
        else:
            origin = event.origins[origin_index]

        picks = [arrival.get_pick() for arrival in origin.arrivals]

        return cls(picks, p_pick_error=p_pick_error,
                   s_pick_error=s_pick_error)

    def __repr__(self):

        lines = ''
        for pick in self.picks:
            if pick.evaluation_status == 'rejected':
                continue

            sensor = pick.sensor
            instrument_identification = pick.waveform_id.channel_code[0:2]
            component = pick.waveform_id.channel_code[-1]
            phase_onset = 'e' if pick.onset in ['emergent', 'questionable'] \
                else 'i'
            phase_descriptor = pick.phase_hint.upper()
            if pick.polarity is None:
                first_motion = '?'
            else:
                first_motion = 'U' if pick.polarity.lower() == 'positive' \
                    else 'D'
            datetime_str = pick.time.strftime('%Y%m%d %H%M %S.%f')

            error_type = 'GAU'
            if pick.phase_hint.upper() == 'P':
                pick_error = f'{self.p_pick_error:0.2e}'
            else:
                pick_error = f'{self.s_pick_error:0.2e}'

            # not implemented
            coda_duration = -1
            amplitude = -1
            period = -1
            phase_weight = 1

            line = f'{sensor:<6s} {instrument_identification:<4s} ' \
                   f'{component:<4s} {phase_onset:1s} ' \
                   f'{phase_descriptor:<6s} {first_motion:1s} ' \
                   f'{datetime_str} {error_type} {pick_error} ' \
                   f'{coda_duration:.2e} {amplitude:.2e} {period:.2e} ' \
                   f'{phase_weight:d}\n'

            lines += line

        return lines

    def write(self, file_name, path='.'):
        with open(Path(path) / file_name, 'w') as file_out:
            file_out.write(str(self))


class LocFiles:
    def __init__(self, velocity_file_path, travel_time_file_path, p_wave=True,
                 swap_bytes_on_input=False):
        """
        Specifies the directory path and file root name (no extension), and
        the wave type identifier for the input velocity grid and output
        time grids.
        :param velocity_file_path: full or relative path and file
        root name (no extension) for input velocity grid (generated by
        program Vel2Grid)
        :type velocity_file_path: str
        :param travel_time_file_path: full or relative path and file
        root name (no extension) for output travel-time and take-off angle
        grids
        :type travel_time_file_path: str
        :param p_wave: p-wave if True, s-wave if False
        :type p_wave: bool
        :param swap_bytes_on_input: flag to indicate if hi and low bytes of
        input velocity grid file should be swapped
        :type swap_bytes_on_input: bool
        """

        self.velocity_file_path = velocity_file_path
        self.travel_time_file_path = travel_time_file_path
        if p_wave:
            self.phase = 'P'
        else:
            self.phase = 'S'

        self.swap_bytes_on_input=int(swap_bytes_on_input)

    def __repr__(self):
        return f'GTFILES {self.velocity_file_path} ' \
               f'{self.travel_time_file_path} {self.phase} ' \
               f'{self.swap_bytes_on_input}'


class GridTimeMode:
    def __init__(self, grid_3d=True, calculate_angles=True):
        """
        Specifies several program run modes.
        :param grid_3d: if True 3D grid if False 2D grid
        :type grid_3d: bool
        :param calculate_angles: if True calculate angles and not if False
        :type calculate_angles: bool
        """

        if grid_3d:
            self.grid_mode = 'GRID3D'
        else:
            self.grid_mode = 'GRID2D'

        if calculate_angles:
            self.angle_mode = 'ANGLES_YES'
        else:
            self.angle_mode = 'ANGLES_NO'

    def __repr__(self):
        return f'GTMODE {self.grid_mode} {self.angle_mode}'


class Srces:
    __valid_measurement_units__ = ['METERS', 'KILOMETERS']

    def __init__(self, sensors=[], units='METERS'):
        """
        specifies a series of source location from an inventory object
        :param sensors: a list of sensors containing at least the location,
        and sensor label
        :type sensors: list of dictionary

        :Example:

        >>> sensor = {'label': 'test', 'x': 1000, 'y': 1000, 'z': 1000,
                      'elev': 0.0}
        >>> sensors = [sensor]
        >>> srces = Srces(srces)

        """

        validate(units, self.__valid_measurement_units__)
        self.units = units

        self.sensors = sensors

    @classmethod
    def from_inventory(cls, inventory):
        """
        create from an inventory object
        :param inventory:
        :type inventory: uquake.core.inventory.Inventory
        """

        srces = []
        for sensor in inventory.sensors:
            srce = {'label': sensor.code,
                    'x': sensor.x,
                    'y': sensor.y,
                    'z': sensor.z,
                    'elev': 0}
            srces.append(srce)

        return cls(srces)

    def add_sensor(self, label, x, y, z, elev=0, units='METERS'):
        """
        Add a single sensor to the source list
        :param label: sensor label
        :type label: str
        :param x: x location relative to geographic origin expressed
        in the units of measurements for sensor/source
        :type x: float
        :param y: y location relative to geographic origin expressed
        in the units of measurements for sensor/source
        :type y: float
        :param z: z location relative to geographic origin expressed
        in the units of measurements for sensor/source
        :type z: float
        :param elev: elevation above z grid position (positive UP) in
        kilometers for sensor (Default = 0)
        :type elev: float
        :param units: units of measurement used to express x, y, and z
        ( 'METERS' or 'KILOMETERS')

        """

        validate(units.upper(), self.__valid_measurement_units__)

        self.sensors.append({'label': label, 'x': x, 'y': y, 'z': z,
                             elev:'elev'})

        self.units = units.upper()

    def __repr__(self):
        line = ""

        for sensor in self.sensors:

            # test if sensor name is shorter than 6 characters

            line += f'GTSRCE {sensor["label"]} XYZ ' \
                    f'{sensor["x"] / 1000:>15.6f} ' \
                    f'{sensor["y"] / 1000:>15.6f} ' \
                    f'{sensor["z"] / 1000:>15.6f} ' \
                    f'0.00\n'

        return line

    @property
    def locs(self):
        seeds = []
        for sensor in self.sensors:
            seeds.append([sensor['x'], sensor['y'], sensor['z']])
        return np.array(seeds)

    @property
    def labels(self):
        seed_labels = []
        for sensor in self.sensors:
            seed_labels.append(sensor['label'])

        return np.array(seed_labels)


__valid_search_grid_type__ = ['MISFIT', 'PROB_DENSITY']


class LocGrid(object):
    def __init__(self, dim_x, dim_y, dim_z, origin_x, origin_y, origin_z,
                 spacing_x, spacing_y, spacing_z, grid_type='PROB_DENSITY',
                 save=False, units='METERS'):
        """
        Specifies the size and other parameters of an initial or nested 3D
        search grid. The order of LOCGRID statements is critical (see Notes).
        repeatable
        :param dim_x: number of grid nodes in the x direction
        :param dim_y: number of grid nodes in the y direction
        :param dim_z: number of grid nodes in the z direction
        :param origin_x: x location of the grid origin in km
        relative to the geographic origin. Use a large, negative value
        ( i.e. -1.0e30 ) to indicate automatic positioning of grid along
        corresponding direction (valid for nested grids only, may not be used
        for initial grid).
        :param origin_y: y location of the grid origin in km
        relative to the geographic origin.
        :param origin_z: z location of the grid origin in km
        relative to the geographic origin.
        :param spacing_x: grid node spacing in kilometers along the x axis
        :param spacing_y: grid node spacing in kilometers along the y axis
        :param spacing_z: grid node spacing in kilometers along the z axis
        :param grid_type: (choice: MISFIT PROB_DENSITY) statistical quantity to
        calculate on grid
        :param save: specifies if the results of the search over this grid
        should be saved to disk (Default: False)
        :type save: bool
        :param units: (choice: 'METERS', 'KILOMETERS') grid units
        (Default 'METERS')
        """

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.origin_z = origin_z
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.spacing_z = spacing_z
        validate(grid_type, __valid_search_grid_type__)
        self.grid_type = grid_type
        self.save = save
        self.units = units

    @classmethod
    def init_from_grid(cls, input_grid, grid_type='PROB_DENSITY', save=True):
        """

        :param input_grid:
        :type input_grid: nlloc.grid.NLLocGrid
        :param grid_type: (choice: MISFIT PROB_DENSITY) statistical quantity to
        calculate on grid
        :param save: specifies if the results of the search over this grid
        should be saved to disk (Default: True)
        :return:
        """
        dims = input_grid.dims
        origin = input_grid.origin
        spacing = input_grid.spacing
        units = input_grid.grid_units

        return cls(dims[0], dims[1], dims[2], origin[0], origin[1], origin[2],
                   spacing[0], spacing[1], spacing[2], units=units,
                   grid_type=grid_type, save=save)

    def __repr__(self):
        div = 1
        if self.units == 'METER':
            div = 1000

        if self.save:
            save_flag = 'SAVE'
        else:
            save_flag = 'NO_SAVE'

        repr = f'LOCGRID {self.dim_x} {self.dim_y} {self.dim_z} ' \
               f'{self.origin_x / div:0.6f} {self.origin_y / div:0.6f} ' \
               f'{self.origin_z / div:0.6f} ' \
               f'{self.spacing_x / div:0.6f} {self.spacing_y / div:0.6f} ' \
               f'{self.spacing_z / div:0.6f} {self.grid_type} {save_flag}\n'

        return repr


class LocQual2Err(object):
    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        line = 'LOCQUAL2ERR'
        for arg in self.args:
            line += f' {arg}'
        return line + '\n'


__observation_file_types__ = ['NLLOC_OBS', 'HYPO71', 'HYPOELLIPSE',
                              'NEIC', 'CSEM_ALERT', 'SIMULPS', 'HYPOCENTER',
                              'HYPODD', 'SEISAN', 'NORDIC', 'NCSN_Y2K_5',
                              'NCEDC_UCB', 'ETH_LOC', 'RENASS_WWW',
                              'RENASS_DEP', 'INGV_BOLL', 'INGV_BOLL_LOCAL',
                              'INGV_ARCH']


class NllocInputFiles:
    def __init__(self, observation_files, travel_time_file_root,
                 output_file_root, observation_file_type='NLLOC_OBS',
                 i_swap_bytes=False, create_missing_folders=True):
        """
        Specifies the directory path and filename for the phase/observation
        files, and the file root names (no extension) for the input time grids
        and the output files.

        the path where the files are to be located is

        :param observation_files: full or relative path and name for
        phase/observations files, mulitple files may be specified with
        standard UNIX "wild-card" characters ( * and ? )
        :type observation_files: str
        :param observation_file_type: (choice: NLLOC_OBS HYPO71 HYPOELLIPSE
        NEIC CSEM_ALERT SIMULPS HYPOCENTER HYPODD SEISAN NORDIC NCSN_Y2K_5
        NCEDC_UCB ETH_LOC RENASS_WWW RENASS_DEP INGV_BOLL
        INGV_BOLL_LOCAL INGV_ARCH) format type for phase/observations files
        (see Phase File Formats) - DEFAULT NLLOC_OBS
        :type observation_file_type: str
        :param travel_time_file_root: full or relative path and file root name
        (no extension) for input time grids.
        :type travel_time_file_root: str
        :param output_file_root: full or relative path and file root name
        (no extension) for output files
        :type output_file_root: str
        :param i_swap_bytes: flag to indicate if hi and low bytes of input
        time grid files should be swapped. Allows reading of travel-time grids
        from different computer architecture platforms during TRANS GLOBAL mode
        location. DEFAULT=False
        :type i_swap_bytes: bool
        :param create_missing_folders: if True missing folder will be created
        """

        # validate if the path exist if the path does not exist the path
        # should be created
        observation_files = Path(observation_files)
        if not observation_files.parent.exists():
            if create_missing_folders:
                logger.warning(f'the path <{observation_files.parent}> does '
                               f'not exist. missing folders will be created')
                observation_files.parent.mkdir(parents=True, exist_ok=True)
            else:
                raise IOError(f'path <{observation_files.parent}> does not '
                              f'exist')

        self.observation_files = observation_files

        travel_time_file_root = Path(travel_time_file_root)
        if not travel_time_file_root.parent.exists():
            if create_missing_folders:
                logger.warning(f'the path <{travel_time_file_root.parent}> '
                               f'does not exist. missing folders will '
                               f'be created')

                travel_time_file_root.parent.mkdir(parents=True, exist_ok=True)
            else:
                raise IOError(f'path <{travel_time_file_root.parent}> does '
                              f'not exist')

        self.travel_time_file_root = travel_time_file_root

        output_file_root = Path(output_file_root)

        if not output_file_root.parent.exists():
            if create_missing_folders:
                logger.warning(f'the path <{output_file_root.parent}> '
                               f'does not exist. missing folders will '
                               f'be created')

                output_file_root.parent.mkdir(parents=True, exist_ok=True)
            else:
                raise IOError(f'path <{output_file_root.parent}> does '
                              f'not exist')

        self.output_file_root = output_file_root

        validate(observation_file_type, __observation_file_types__)
        self.observation_file_type = observation_file_type

        self.i_swap_bytes = i_swap_bytes

    def __repr__(self):
        line = f'LOCFILES {self.observation_files} ' \
               f'{self.observation_file_type} {self.travel_time_file_root} ' \
               f'{self.output_file_root} {int(self.i_swap_bytes)}\n'
        return line


def read_hypocenter_file(filename, units='METER'):

    validate(units, __valid_units__)
    with open(filename, 'r') as hyp_file:
        all_lines = hyp_file.readlines()
        hyp = [line.split() for line in all_lines if 'HYPOCENTER' in line][0]
        geo = [line.split() for line in all_lines if 'GEOGRAPHIC' in line][0]

        s = int(np.floor(float(geo[7])))
        us = int((float(geo[7]) - s) * 1e6)

        if s < 0:
            s = 0

        if us < 0:
            us = 0

        tme = datetime(int(geo[2]), int(geo[3]), int(geo[4]),
                       int(geo[5]), int(geo[6]), s, us)
        tme = UTCDateTime(tme)

        hyp_x = float(hyp[2]) * 1000
        hyp_y = float(hyp[4]) * 1000
        hyp_z = float(hyp[6]) * 1000

        return tme, hyp_x, hyp_y, hyp_z


def read_scatter_file(filename):
    """
    :param filename: name of the scatter file to read
    :return: a numpy array of the points in the scatter file
    """

    f = open(filename, 'rb')

    n_samples = unpack('i', f.read(4))[0]
    unpack('f', f.read(4))
    unpack('f', f.read(4))
    unpack('f', f.read(4))

    points = []

    for k in range(0, n_samples):
        x = unpack('f', f.read(4))[0] * 1000
        y = unpack('f', f.read(4))[0] * 1000
        z = unpack('f', f.read(4))[0] * 1000
        pdf = unpack('f', f.read(4))[0]

        points.append([x, y, z, pdf])

    return np.array(points)


# def read_nlloc_hypocenter_file(filename, picks=None,
#                                evaluation_mode='automatic',
#                                evaluation_status='preliminary'):
#     """
#     read NLLoc hypocenter file into an events catalog
#     :param filename: path to NLLoc hypocenter filename
#     :type filename: str
#     :return: seismic catalogue
#     :rtype: ~uquake.core.event.Catalog
#     """
#     cat = Catalog()
#
#     with open(filename) as hyp_file:
#
#         all_lines = hyp_file.readlines()
#         hyp = [line.split() for line in all_lines if 'HYPOCENTER' in line][0]
#         stat = [line.split() for line in all_lines if 'STATISTICS' in line][0]
#         geo = [line.split() for line in all_lines if 'GEOGRAPHIC' in line][0]
#         qual = [line.split() for line in all_lines if 'QUALITY' in line][0]
#         search = [line.split() for line in all_lines if 'SEARCH' in line][0]
#         sign = [line.split() for line in all_lines if 'SIGNATURE' in line][0]
#
#         s = int(np.floor(float(geo[7])))
#         us = int((float(geo[7]) - s) * 1e6)
#
#         if s < 0:
#             s = 0
#
#         if us < 0:
#             us = 0
#
#         tme = datetime(int(geo[2]), int(geo[3]), int(geo[4]),
#                        int(geo[5]), int(geo[6]), s, us)
#         tme = UTCDateTime(tme)
#
#         if 'REJECTED' in all_lines[0]:
#             evaluation_status = 'rejected'
#             logger.warning('Event located on grid boundary')
#         else:
#             evaluation_status = evaluation_status
#
#         hyp_x = float(hyp[2]) * 1000
#         hyp_y = float(hyp[4]) * 1000
#         hyp_z = float(hyp[6]) * 1000
#
#         method = 'NLLOC'
#
#         creation_info = obspy.core.event.CreationInfo(
#             author='uquake', creation_time=UTCDateTime.now())
#
#         origin = Origin(x=hyp_x, y=hyp_y, z=hyp_z, time=tme,
#                         evaluation_mode=evaluation_mode,
#                         evaluation_status=evaluation_status,
#                         epicenter_fixed=0, method_id=method,
#                         creation_info=creation_info)
#
#         xminor = np.cos(float(stat[22]) * np.pi / 180) * np.sin(float(stat[20])
#                                                                 * np.pi / 180)
#         yminor = np.cos(float(stat[22]) * np.pi / 180) * np.cos(float(stat[20])
#                                                                 * np.pi / 180)
#         zminor = np.sin(float(stat[22]) * np.pi / 180)
#         xinter = np.cos(float(stat[28]) * np.pi / 180) * np.sin(float(stat[26])
#                                                                 * np.pi / 180)
#         yinter = np.cos(float(stat[28]) * np.pi / 180) * np.cos(float(stat[26])
#                                                                 * np.pi / 180)
#         zinter = np.sin(float(stat[28]) * np.pi / 180)
#
#         minor = np.array([xminor, yminor, zminor])
#         inter = np.array([xinter, yinter, zinter])
#
#         major = np.cross(minor, inter)
#
#         major_az = np.arctan2(major[0], major[1])
#         major_dip = np.arctan(major[2] / np.linalg.norm(major[0:2]))
#         # MTH: obspy will raise error if you try to set float attr to nan below
#
#         if np.isnan(major_az):
#             major_az = None
#
#         if np.isnan(major_dip):
#             major_dip = None
#
#         # obspy will complain if we use anything other then the exact type
#         # it expects. Cannot extend, cannot even import from elsewhere!
#         el = obspy.core.event.ConfidenceEllipsoid()
#         el.semi_minor_axis_length = float(stat[24]) * 1000
#         el.semi_intermediate_axis_length = float(stat[30]) * 1000
#         el.semi_major_axis_length = float(stat[32]) * 1000
#         el.major_axis_azimuth = major_az
#         el.major_axis_plunge = major_dip
#
#         # obsy will complain... see above
#         ou = obspy.core.event.OriginUncertainty()
#         ou.confidence_ellipsoid = el
#
#         origin.origin_uncertainty = ou
#
#         TravelTime = False
#         oq = obspy.core.event.OriginQuality()
#         arrivals = []
#         stations = []
#         phases = []
#         oq.associated_phase_count = 0
#
#         for line in all_lines:
#             if 'PHASE ' in line:
#                 TravelTime = True
#
#                 continue
#             elif 'END_PHASE' in line:
#                 TravelTime = False
#
#                 continue
#
#             if TravelTime:
#                 tmp = line.split()
#                 stname = tmp[0]
#
#                 phase = tmp[4]
#                 res = float(tmp[16])
#                 weight = float(tmp[17])
#                 sx = float(tmp[18])
#                 sy = float(tmp[19])
#                 sz = float(tmp[20])
#     # MTH: In order to not get default = -1.0 for ray azimuth + takeoff here, you
#     #      need to set ANGLES_YES in the NLLOC Grid2Time control file. Then, when Grid2Time runs, it
#     #      will also create the angle.buf files in NLLOC/run/time and when NLLoc runs, it will interpolate
#     #      these to get the ray azi + takeoff and put them on the phase line of last.hyp
#     # However, the NLLoc generated takeoff angles look to be incorrect (< 90 deg),
#     #  likely due to how OT vertical up convention wrt NLLoc.
#     # So instead, use the spp generated files *.azimuth.buf and *.takeoff.buf to overwrite these later
#     #      15       16       17              18  19       20          21       22     23 24
#     #  >   TTpred    Res       Weight    StaLoc(X  Y         Z)        SDist    SAzim  RAz  RDip RQual    Tcorr
#     #  >  0.209032  0.002185    1.2627  651.3046 4767.1881    0.9230    0.2578 150.58  -1.0  -1.0  0     0.0000
#
#                 azi = float(tmp[22])  # Set to SAzim since that is guaranteed to be set
#                 # azi = float(tmp[23])
#                 toa = float(tmp[24])
#
#                 dist = np.linalg.norm([sx * 1000 - origin.x,
#                                        sy * 1000 - origin.y,
#                                        sz * 1000 - origin.z])
#
#                 '''
#                 MTH: Some notes about the NLLOC output last.hyp phase lines:
#                     1. SDist - Is just epicentral distance so does not take into account dz (depth)
#                                So 3D Euclidean dist as calculated above will be (much) larger
#                     2. SAzim - NLLOC manual says this is measured from hypocenter CCW to station
#                                But it looks to me like it's actually clockwise!
#                     3. RAz - "Ray take−off azimuth at maximum likelihood hypocenter in degrees CCW from North"
#                               In a true 3D model (e.g., lateral heterogeneity) this could be different
#                               than SAzim.
#                               Have to set: LOCANGLES ANGLES_YES 5 to get the angles, otherwise defaults to -1
#                               Probably these are also actually measured clockwise from North
#
#                 distxy = np.linalg.norm([sx * 1000 - origin.x,
#                                          sy * 1000 - origin.y])
#
#                 sdist = float(tmp[21])
#                 sazim = float(tmp[22])
#                 raz = float(tmp[23])
#                 rdip = float(tmp[24])
#
#                 print("Scan last.hyp: sta:%3s pha:%s dist_calc:%.1f sdist:%.1f sazim:%.1f raz:%.1f rdip:%.1f" % \
#                       (stname, phase, distxy, sdist*1e3, sazim, raz, rdip))
#
#                 '''
#
#                 arrival = Arrival()
#                 arrival.phase = phase
#                 arrival.distance = dist
#                 arrival.time_residual = res
#                 arrival.time_weight = weight
#                 arrival.azimuth = azi
#                 arrival.takeoff_angle = toa
#                 arrivals.append(arrival)
#
#                 for pick in picks:
#                     if ((pick.phase_hint == phase) and (
#                             pick.waveform_id.station_code == stname)):
#
#                         arrival.pick_id = pick.resource_id.id
#
#                 stations.append(stname)
#                 phases.append(phase)
#
#                 oq.associated_phase_count += 1
#
#         stations = np.array(stations)
#
#         points = read_scatter_file(filename.replace('.hyp', '.scat'))
#
#         origin.arrivals = [arr for arr in arrivals]
#         origin.scatter = points
#
#         oq.associated_station_count = len(np.unique(stations))
#
#         oq.used_phase_count = oq.associated_phase_count
#         oq.used_station_count = oq.associated_station_count
#         oq.standard_error = float(qual[8])
#         oq.azimuthal_gap = float(qual[12])
#         origin.quality = oq
#
#     return origin


# def calculate_uncertainty(event, base_directory, base_name, perturbation=5,
#                           pick_uncertainty=1e-3):
#     """
#     :param event: event
#     :type event: uquake.core.event.Event
#     :param base_directory: base directory
#     :param base_name: base name for grids
#     :param perturbation:
#     :return: uquake.core.event.Event
#     """
#
#     if hasattr(event.preferred_origin(), 'scatter'):
#         scatter = event.preferred_origin().scatter[:, 1:].copy()
#         scatter[:, 0] -= np.mean(scatter[:, 0])
#         scatter[:, 1] -= np.mean(scatter[:, 1])
#         scatter[:, 2] -= np.mean(scatter[:, 2])
#         u, d, v = np.linalg.svd(scatter)
#         uncertainty = np.sqrt(d)
#
#         h = np.linalg.norm(v[0, :-1])
#         vert = v[0, -1]
#         major_axis_plunge = np.arctan2(-vert, h)
#         major_axis_azimuth = np.arctan2(v[0, 0], v[0, 1])
#         major_axis_rotation = 0
#
#         ce = obspy.core.event.ConfidenceEllipsoid(
#              semi_major_axis_length=uncertainty[0],
#              semi_intermediate_axis_length=uncertainty[1],
#              semi_minor_axis_length=uncertainty[2],
#              major_axis_plunge=major_axis_plunge,
#              major_axis_azimuth=major_axis_azimuth,
#              major_axis_rotation=major_axis_rotation)
#         ou = obspy.core.event.OriginUncertainty(confidence_ellipsoid=ce)
#         return ou
#
#     narr = len(event.preferred_origin().arrivals)
#
#     # initializing the frechet derivative
#     Frechet = np.zeros([narr, 3])
#
#     event_loc = np.array(event.preferred_origin().loc)
#
#     for i, arrival in enumerate(event.preferred_origin().arrivals):
#         pick = arrival.pick_id.get_referred_object()
#         station_code = pick.waveform_id.station_code
#         phase = arrival.phase
#
#         # loading the travel time grid
#         filename = '%s/time/%s.%s.%s.time' % (base_directory,
#                                               base_name, phase, station_code)
#
#         tt = read_grid(filename, format='NLLOC')
#         # spc = tt.spacing
#
#         # build the Frechet derivative
#
#         for dim in range(0, 3):
#             loc_p1 = event_loc.copy()
#             loc_p2 = event_loc.copy()
#             loc_p1[dim] += perturbation
#             loc_p2[dim] -= perturbation
#             tt_p1 = tt.interpolate(loc_p1, grid_coordinate=False)
#             tt_p2 = tt.interpolate(loc_p2, grid_coordinate=False)
#             Frechet[i, dim] = (tt_p1 - tt_p2) / (2 * perturbation)
#
#     hessian = np.linalg.inv(np.dot(Frechet.T, Frechet))
#     tmp = hessian * pick_uncertainty ** 2
#     w, v = np.linalg.eig(tmp)
#     i = np.argsort(w)[-1::-1]
#     # for the angle calculation see
#     # https://en.wikipedia.org/wiki/Euler_angles#Tait-Bryan_angles
#     X = v[:, i[0]]  # major
#     Y = v[:, i[1]]  # intermediate
#     # Z = v[:, i[2]]  # minor
#
#     X_H = np.sqrt(X[0] ** 2 + X[1] ** 2)
#     major_axis_plunge = np.arctan2(X[2], X_H)
#     major_axis_azimuth = np.arctan2(X[1], X[0])
#     major_axis_rotation = 0
#
#     # major_axis_plunge = np.arcsin(X[2] / np.sqrt(1 - X[2] ** 2))
#     # major_axis_azimuth = np.arcsin(X[1] / np.sqrt(1 - X[2] ** 2))
#     # major_axis_rotation = np.arcsin(-X[2])
#     ce = obspy.core.event.ConfidenceEllipsoid(
#         semi_major_axis_length=w[i[0]],
#         semi_intermediate_axis_length=w[i[1]],
#         semi_minor_axis_length=w[i[2]],
#         major_axis_plunge=major_axis_plunge,
#         major_axis_azimuth=major_axis_azimuth,
#         major_axis_rotation=major_axis_rotation)
#     ou = obspy.core.event.OriginUncertainty(confidence_ellipsoid=ce)
#
#     return ou


# def read_scatter_file(filename):
#     """
#     :param filename: name of the scatter file to read
#     :return: a numpy array of the points in the scatter file
#     """
#
#     f = open(filename, 'rb')
#
#     nsamples = unpack('i', f.read(4))[0]
#     unpack('f', f.read(4))
#     unpack('f', f.read(4))
#     unpack('f', f.read(4))
#
#     points = []
#
#     for k in range(0, nsamples):
#         x = unpack('f', f.read(4))[0] * 1000
#         y = unpack('f', f.read(4))[0] * 1000
#         z = unpack('f', f.read(4))[0] * 1000
#         pdf = unpack('f', f.read(4))[0]
#
#         points.append([x, y, z, pdf])
#
#     return np.array(points)
