#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

import math


class PlanarPose(object):
    """3D Pose representation in Cartesian or Polar coordinate system on a plane.
    """

    def __str__(self):
        return f'X: {self.x()} Y: {self.y()}, RZ: {self.rz()}'

    def __init__(self, c1, c2, c3=None):
        """ Creates Pose instance with cartesian coordinates if thee arguments are provided,
        or polar coordinates if two arguments are provided
            Args:
                c1(float): x coordinate (Cartesian), distance (Polar)
                c2(float): y coordinate (Cartesian), angle(Polar)
                c3(float): rotation angle (Cartesian)
        """
        self.__x = c1
        if c3:
            self.__y = c2
            self.__rz = c3
        else:
            self.__y = 0
            self.__rz = c2

    def x(self):
        """
            Returns:
                bool: Returns position in X axis.
        """
        return self.__x

    def y(self):
        """
            Returns:
                bool: Returns position in Y axis.
        """
        return self.__y

    def rz(self):
        """
            Returns:
                bool: Rotation around Z axis.
        """
        return self.__rz

    def almostEqual(self, pose, tolerance=None):
        """Equal operation with the tolerance.

            Args:
                pose(PlanarPose): pose to compare with
                tolerance(PlanarPose): tolerance, default value is Pose(0.1, 0.1, 0.1)

            Returns:
                True if pose is within the tolerance.
        """

        if not tolerance:
            tolerance = PlanarPose(0.1, 0.1, 0.1)

        diff_x = math.fabs(self.x() - pose.x())
        diff_y = math.fabs(self.y() - pose.y())
        diff_rz = math.fabs(math.atan2(math.sin(self.rz() - pose.rz()), math.cos(self.rz() - pose.rz())))
        return (diff_x <= tolerance.x()) and (diff_y <= tolerance.y()) and (diff_rz <= tolerance.rz())
