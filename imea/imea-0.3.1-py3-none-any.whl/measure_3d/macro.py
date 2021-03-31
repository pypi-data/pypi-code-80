"""3-dimensional macrodescriptors."""
import warnings


import numpy as np
from scipy.spatial import ConvexHull
from skimage import measure

from imea import measure_2d
from imea.tools import project, rotate


def volume(img_3d_equalspace, spatial_resolution):
    """Calculate volume.

    Parameters
    ----------
    img_3d_equalspace : numpy.ndarray, type float
        2-dimensional grayscale heightmap of single object with equal spacing, i.e. dx = dy = dz.
        Pixels not showing the pixel should be 0.
    spatial_resolution : float
        Spatial resolution of `img_3d_equalspace` in [mm/Voxel].
        The following must be true: spatial_resolution == dx == dy == dz.
    Returns
    -------
    float
        - `volume` (float):
            Volume in [mm^3].
    """
    assert img_3d_equalspace.ndim == 2,\
        "`img_3d_equalspace` must be 2-dimensional array (heightmap)."

    volume = np.sum(img_3d_equalspace.ravel())

    if volume == 0:
        warnings.warn("`img_3d_equalspace` is empty.")

    return volume * spatial_resolution**3


def volume_convexhull(convex_hull, spatial_resolution):
    """Calculate volume of convex hull.

    Parameters
    ----------
    convex_hull : scipy.spatial.ConvexHull
        Convex Hull.
    spatial_resolution : float
        Spatial resolution of `convex_hull` in [mm/Voxel].

    Returns
    -------
    float
        - `volume_convexhull` (float):
            Volume of convex hull in [mm^3].
    """
    return convex_hull.volume * spatial_resolution**3


def volume_equivalent_diameter(volume):
    """Calculate volume equivalent diameter.

    Parameters
    ----------
    volume : float
        Volume.

    Returns
    -------
    float
        - `volume_equivalent_diameter` (float):
            Volume-equivalent diameter.
    """
    return np.cbrt(6 * volume/np.pi)


def surfacearea_convexhull(convex_hull, spatial_resolution):
    """Calculate surface area of convex hull.

    Parameters
    ----------
    convex_hull : scipy.spatial.ConvexHull
        Convex Hull.
    spatial_resolution : float
        Spatial resolution of `convex_hull` in [mm/Voxel].

    Returns
    -------
    float
        - `surface_area` (float):
            Surface area of convex hull in [mm^2].
    """
    return convex_hull.area * spatial_resolution**2


def surfacearea_equivalent_diameter(surface_area):
    """Calculate surfacearea-equivalent diameter.

    Parameters
    ----------
    surface_area : float
        Surface area.

    Returns
    -------
    float
        - `surfacearea_equivalent_diameter` (float):
            Surface area-equivalent diameter.
    """
    return np.sqrt(surface_area/np.pi)


def min_3d_bounding_box(img_3d_equalspace, spatial_resolution):
    """Calculate minimal 3-dimensional bounding box from a 3D grayscale image.

    Parameters
    ----------
    img_3d_equalspace : numpy.ndarray, type float
        2-dimensional grayscale heightmap of single object with equal spacing, i.e. dx = dy = dz.
        Pixels not showing the pixel should be 0.
    spatial_resolution : float
        Spatial resolution of `img_3d_equalspace` in [mm/Voxel].
        The following must be true: spatial_resolution == dx == dy == dz.

    Returns
    -------
    tuple
        - `length` (float):
            Length of minimal 3-dimensional bounding box.
        - `width` (float):
            Width of minimal 3-dimensional bounding box.
        - `height` (float):
            Height of minimal 3-dimensional bounding box.

    Notes
    -----
    `length` and `width` are identical to the 2d bounding box.
    `height` is the maximum height in z-direction.
    """
    bw = img_3d_equalspace > 0
    length, width, _, _ = measure_2d.macro.min_2d_bounding_box(bw)
    height = np.max(img_3d_equalspace.ravel())

    width = width * spatial_resolution
    length = length * spatial_resolution
    height = height * spatial_resolution

    return width, length, height


def feret_and_max_dimensions_3d(convex_hull, spatial_resolution, dalpha=9):
    """Calculates 3D feret diameter (min, max) and
    max dimensions (x_max, y_max, z_max) [1].

    Parameters
    ----------
    convex_hull : scipy.spatial.ConvexHull
        3D convex hull.
    spatial_resolution : float
        Spatial resolution of `convex_hull` in [mm].
    dalpha : int, optional
        Angle in degrees by which `convex_hull` at each iteration,
        by default 9.

    Returns
    -------
    tuple
        - `feret_3d_max` (float):
            Max feret diameter.
        - `feret_3d_min` (float):
            Min feret diameter.
        - `x_max_3d` (float):
            x_max (equal to max_feret) [1].
        - `y_max_3d` (float):
            y_max (orthogonal to x_max) [1].
        - `z_max_3d` (float):
            z_max (orthogonal to x_max and y_max) [1].

    References
    ----------
    [1] M. Steuer (2010). "Serial classification".
    In: AT Mineral Processing 51(1).
    """
    p_3d = convex_hull.points[convex_hull.vertices]

    # feret diameters
    angles_x = np.arange(0, 180, dalpha)
    angles_y = np.arange(0, 180, dalpha)

    n_angles_x = len(angles_x)
    n_angles_y = len(angles_y)

    calipers = np.zeros((n_angles_x, n_angles_y))

    for i, a_x in enumerate(angles_x):
        p_3d_rot = rotate.apply(p_3d, rotate.Rx(a_x))
        p_2d = project.xyz_to_xz(p_3d_rot)
        for j, a_y in enumerate(angles_y):
            p_2d_rot = rotate.apply(p_2d, rotate.R_2d(a_y))
            calipers[i, j] = _caliper_2d(p_2d_rot, axis=1)

    feret_3d_max = np.max(calipers.ravel())
    feret_3d_min = np.min(calipers.ravel())

    # x_max
    x_max_3d = feret_3d_max

    # y_max
    # rotate, s. t. x_max is parallel to x-axis
    idxs_max_feret = np.where(calipers == feret_3d_max)
    angle_x_max_feret = angles_x[idxs_max_feret[0][0]]
    angle_y_max_feret = angles_y[idxs_max_feret[1][0]]

    p3d_ymax = np.copy(p_3d)
    p3d_ymax = rotate.apply(p3d_ymax, rotate.Rx(angle_x_max_feret))
    p3d_ymax = rotate.apply(p3d_ymax, rotate.Ry(angle_y_max_feret))

    angles_x_ymax = np.arange(0, 180, dalpha)
    ymax_list = np.zeros_like(angles_x_ymax)

    for a_x in angles_x_ymax:
        p3d_ymax_rot = rotate.apply(p3d_ymax, rotate.Rx(a_x))
        p2d_ymax_rot = project.xyz_to_xz(p3d_ymax_rot)
        ymax_list[i] = _max_chord_from_2d_pointcloud(
            p2d_ymax_rot, axis=0)

    y_max_3d = np.max(ymax_list)
    idx = np.argmax(ymax_list)
    angle_x_ymax = angles_x_ymax[idx]

    # z_max
    p3d_zmax = np.copy(rotate.apply(p3d_ymax, rotate.Rx(angle_x_ymax)))
    p2d_zmax = project.xyz_to_yz(p3d_zmax)
    z_max_3d = _max_chord_from_2d_pointcloud(p2d_zmax, axis=0)

    if y_max_3d < z_max_3d:
        y_max_3d, z_max_3d = z_max_3d, y_max_3d

    # apply spatial resolution
    feret_3d_max = feret_3d_max * spatial_resolution
    feret_3d_min = feret_3d_min * spatial_resolution

    x_max_3d = x_max_3d * spatial_resolution
    y_max_3d = y_max_3d * spatial_resolution
    z_max_3d = z_max_3d * spatial_resolution

    return feret_3d_max, feret_3d_min, x_max_3d, y_max_3d, z_max_3d


def _bw_of_2d_convexhull(pointcloud_convexhull):
    """Transforms 2d convex pointcloud into binary image.

    Parameters
    ----------
    pointcloud_convexhull : numpy.ndarray, type float
        2-dimensional pointcloud representing convex hull of shape (n, 2).

    Returns
    -------
    numpy.ndarray, type bool
        - `bw_convexhull` (numpy.ndarray, type bool):
            Binary image of 2d convex hull.
    """

    # move points to intervall [0, inf]
    min_values = np.min(pointcloud_convexhull, axis=0)
    x = np.array([min_values, np.zeros_like(min_values)])
    min_values = np.min(x, axis=0)
    min_values_abs = np.abs(min_values)
    pointcloud_convexhull = pointcloud_convexhull + min_values_abs

    # transform to binary image
    gridsize = np.ceil(np.max(pointcloud_convexhull, axis=0)).astype('int')
    bw_convexhull = measure.grid_points_in_poly(
        gridsize, pointcloud_convexhull)

    return bw_convexhull


def _caliper_2d(pts_2d, axis=1):
    """Apply 2d caliper at pointcloud along `axis`.

    Parameters
    ----------
    pts_2d : numpy.ndarray, type float
        2D pointcloud of shape `(n, 2)`.
    axis : {0, 1}, optional
        Axis along which caliper is measured, by default 1.

    Returns
    -------
    float
        - `caliper` (float):
            Caliper distance.
    """
    return np.max(pts_2d[:, axis]) - np.min(pts_2d[:, axis])


def _max_chord_from_2d_pointcloud(pointcloud_2d, axis=0):
    """Calculate maximum chord from 2d pointcloud based on convex hull.

    Parameters
    ----------
    pointcloud_2d : numpy.ndarray, type float
        2-dimensional pointcloud representing object of shape (n, 2)
    axis : int, optional
        Axis along which max chord is measured, by default 0.

    Returns
    -------
    float
        - `max_chord` (float):
            Max chord of `pointcloud_2d` in measurement direction.
    """
    if axis == 0:
        # Rotate by 90 degrees, since chords are measurement
        # in 2D y not 2D x-direction (see function calc_chords_2d)
        pointcloud_2d = rotate.apply(pointcloud_2d, rotate.R_2d(90))

    # Get 2D convex hull
    convex_hull = ConvexHull(pointcloud_2d)
    convex_pointcloud = convex_hull.points[convex_hull.vertices]

    # determine chords
    bw = _bw_of_2d_convexhull(convex_pointcloud)
    chords, _ = measure_2d.statistical_length.find_all_chords(bw)
    max_chord = np.max(chords)

    return max_chord
