"""Helping functions for 3-dimensional shape measurements."""

import numpy as np
from scipy.spatial import ConvexHull
from skimage import measure

from imea import measure_2d
from imea.tools import rotate


def compute_convexhull(img_3d_equalspace):
    """Calculate convex hull from 3d image.

    Parameters
    ----------
    img_3d_equalspace : numpy.ndarray, type float
        2-dimensional grayscale heightmap of single object with equal spacing, i.e. dx = dy = dz.
        Pixels not showing the pixel should be 0.

    Returns
    -------
    scipy.spatial.ConvexHull
        - `convex_hull` (scipy.spatial.ConvexHull):
            Convex hull.
    """
    bw = img_3d_equalspace > 0

    (x, y) = np.where(bw)
    z_top = img_3d_equalspace[x, y]
    z_bottom = np.zeros_like(x)
    x = np.concatenate([x]*2)
    y = np.concatenate([y]*2)
    z = np.concatenate([z_top, z_bottom], axis=0)

    # To transform the indexes from above into real coordinates
    # we need to make the region + 0.5 greater in every direction
    # We do this by applying shift in every diagonal direction and then computing the convex hull

    x_all = []
    y_all = []
    z_all = []
    shifts = np.array([[0.5, 0.5],
                       [-0.5, 0.5],
                       [0.5, -0.5],
                       [-0.5, -0.5]])
    for shift in shifts:
        x_shifted = x + shift[0]
        x_all.append(x_shifted)

        y_shifted = y + shift[1]
        y_all.append(y_shifted)

        # z-coordinate remains unchanged
        z_all.append(z)

    x_all = np.concatenate(x_all)
    y_all = np.concatenate(y_all)
    z_all = np.concatenate(z_all)

    points_3d = np.column_stack([x_all, y_all, z_all])
    return ConvexHull(points_3d)
