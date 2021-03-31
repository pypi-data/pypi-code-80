"""Helping functions for 2-dimensional shape measurements."""

import warnings

import cv2
import numpy as np
from skimage import measure


def find_contour(bw):
    """Find external contour points of an object shape.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    numpy.ndarray, type int
        - `contour` (numpy.ndarray, type int):
            2-dimensional array of contourpoints
            in shape `[[x0, y0], [x1, y1], [x2, y2], ...]`.
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    # the try/except case handles different versions of cv2 (some return 2 some return 3 values)
    try:
        contour_cv2, _ = cv2.findContours(bw.astype('uint8'),
                                          cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_NONE)
    except ValueError:
        _, contour_cv2, _ = cv2.findContours(bw.astype('uint8'),
                                             cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_NONE)

    # transform array of contour points and change coordinate system to (x, y)
    contour = _cv2contour_to_array(contour_cv2)

    return contour


def _array_to_cv2contour(contour):
    """Transform contour points from array to cv2 representation.

    Parameters
    ----------
    contour : numpy.ndarray, type int
        2-dimensional array of contourpoints
        in shape `[[x0, y0], [x1, y1], [x2, y2], ...]`.

    Returns
    -------
    list
        - `contour_cv2` (list):
            Contour points as represented by `cv2`:
            `[[[[y0, x0]], [[y1, x1]], [[y2, x2]], ...]]`
    """

    contour_cv2 = np.zeros((contour.shape[0],
                            1,
                            contour.shape[1]),
                           dtype='int')

    contour_cv2[:, 0, 0] = contour[:, 1]
    contour_cv2[:, 0, 1] = contour[:, 0]

    contour_cv2 = [contour_cv2]

    return contour_cv2


def _cv2contour_to_array(contour_cv2):
    """Transform contour points from cv2 to array representation.

    Parameters
    ----------
    contour_cv2 : list
        Contour points as represented by `cv2`:
        `[[[[y0, x0]], [[y1, x1]], [[y2, x2]], ...]]`

    Returns
    -------
    numpy.ndarray, type int
        - `contour` (numpy.ndarray, type int):
            2-dimensional array of contourpoints
            in shape `[[x0, y0], [x1, y1], [x2, y2], ...]`.
    """

    if len(contour_cv2) == 0:
        warnings.warn("`contour_cv2` is empty --> return empty array.")
        return np.zeros((0, 2))
    # unpack list
    contour_cv2 = contour_cv2[0]

    # transform array of contour points and change coordinate system to (x, y)
    contour = np.zeros(
        (contour_cv2.shape[0], contour_cv2.shape[2]), dtype='int')
    contour[:, 0] = contour_cv2[:, 0, 1]
    contour[:, 1] = contour_cv2[:, 0, 0]

    return contour


def skimage_measurements(bw):
    """Calculate object shape measurements based on `skimage.measure.regionprops`.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `area_projection` (int):
            Projection area.
        - `perimeter` (float):
            Perimeter.
        - `area_filled` (int):
            Filled area.
        - `area_convex` (int):
            Convex area.
        - `major_axis_length` (float):
            Major axis length.
        - `minor_axis_length` (float):
            Minor axis length.
        - `centroid` (numpy.ndarray, type float):
            Centroid in shape `[x, y]`.
        - `coords` (numpy.ndarray, type int):
            2-dimensional array of object coordinates
            in shape `[[x0, y0], [x1, y1], ...]`.
        - `bw_cropped` (numpy.ndarray, type bool):
            Cropped version of `bw`.
        - `bw_convex` (numpy.ndarray, type bool):
            Cropped 2-dimensional convex binary image of `bw`.

    Notes
    -----
    Extracts only shape measurement of largest object in `bw_org`,
    since multi object shape extraction is handled by higher
    functions in **imea**.
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")
        return 0, 0, 0, 0, 0, 0, np.array([]), np.array([]),\
            np.zeros_like(bw, dtype='bool'), np.zeros_like(bw, dtype='bool')

    labels = measure.label(bw)
    props = measure.regionprops(labels, intensity_image=bw)

    perimeter = props[0].perimeter
    area_projection = props[0].area
    area_filled = props[0].filled_area
    area_convex = props[0].convex_area
    major_axis_length = props[0].major_axis_length
    minor_axis_length = props[0].minor_axis_length
    centroid = np.array(props[0].centroid)
    coords = props[0].coords
    bw_cropped = props[0].image
    bw_convex = props[0].convex_image

    return perimeter, area_projection, area_filled, area_convex, major_axis_length, \
        minor_axis_length, centroid, coords, bw_cropped, bw_convex
