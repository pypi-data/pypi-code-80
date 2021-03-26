"""Helping functions to rotate points around a given axis."""

import numpy as np


def apply(pts, R):
    """Apply rotation matrix `R` to pointcloud `pts`.

    Parameters
    ----------
    pts : numpy.ndarray
        Points to be rotated of shape `(n,d)`,
        where `n` is the number of points and `d` the number of dimensions.
    R : numpy.ndarray
        Rotation matrix of shape `(d,d)`.

    Returns
    -------
    numpy.ndarray
        - `out` : numpy.ndarray
            Rotated points.
    """
    return np.dot(pts, R)


def Rx(angle_in_degrees):
    """3D rotation matrix for rotating around x-axis.

    Parameters
    ----------
    angle_in_degrees : float
        Rotation angle around x-axis in degrees.

    Returns
    -------
    numpy.ndarray
        - `Rx` (numpy.ndarray):
            3D Rotation matrix.
    """
    angle_in_rad = angle_in_degrees/180 * np.pi
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(angle_in_rad), -np.sin(angle_in_rad)],
                   [0, np.sin(angle_in_rad), np.cos(angle_in_rad)]])
    return Rx


def Ry(angle_in_degrees):
    """3D rotation matrix for rotating around y-axis.

    Parameters
    ----------
    angle_in_degrees : float
        Rotation angle around y-axis in degrees.

    Returns
    -------
    numpy.ndarray
        - `Ry` (numpy.ndarray):
            3D Rotation matrix.
    """
    angle_in_rad = angle_in_degrees/180 * np.pi
    Ry = np.array([[np.cos(angle_in_rad), 0, np.sin(angle_in_rad)],
                   [0, 1, 0],
                   [-np.sin(angle_in_rad), 0, np.cos(angle_in_rad)]])
    return Ry


def Rz(angle_in_degrees):
    """3D rotation matrix for rotating around z-axis.

    Parameters
    ----------
    angle_in_degrees : float
        Rotation angle around z-axis in degrees.

    Returns
    -------
    numpy.ndarray
        - `Rz` (numpy.ndarray):
            3D Rotation matrix.
    """
    angle_in_rad = angle_in_degrees/180 * np.pi
    Rz = np.array([[np.cos(angle_in_rad), -np.sin(angle_in_rad), 0],
                   [np.sin(angle_in_rad), np.cos(angle_in_rad), 0],
                   [0, 0, 1]])
    return Rz


def R_2d(angle_in_degrees):
    """2D rotation matrix.

    Parameters
    ----------
    angle_in_degrees : float
        Rotation angle in degrees.

    Returns
    -------
    numpy.ndarray
        - `R` (numpy.ndarray):
            2D Rotation matrix.
    """
    angle_in_rad = angle_in_degrees/180 * np.pi
    R = np.array([[np.cos(angle_in_rad), -np.sin(angle_in_rad)],
                  [np.sin(angle_in_rad), np.cos(angle_in_rad)]])
    return R
