"""2-dimensional macrodescriptors."""

import warnings

import cv2
import numpy as np
from scipy import spatial
from skimage import measure

from imea import measure_2d


def min_2d_bounding_box(bw):
    """Calculate minimal 2-dimensional bounding box of an binary image.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `length` (float):
            Length of minimal 2-dimensional bounding box.
        - `width` (float):
            Width of minimal 2-dimensional bounding box.
        - `center` (numpy.ndarray, type float):
            Center of 2-dimensional minimal bounding box in shape `[x, y]`.
        - `cornerpoints` (numpy.ndarray, type float):
            2-dimensional array of four cornerpoints of the minimal bounding box
            in shape `[[x0, y0], [x1, y1], [x2, y2], [x3, y3]]`.
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    contour = measure_2d.utils.find_contour(bw)
    length, width, center, cornerpoints = _min_2d_bounding_box_from_contour(
        contour)

    return length, width, center, cornerpoints


def _min_2d_bounding_box_from_contour(contour):
    """Calculate minimal 2-dimensional bounding box of an image based on contours.

    Parameters
    ----------
    contour : numpy.ndarray, type int
        2-dimensional array of contourpoints
        in shape `[[x0, y0], [x1, y1], [x2, y2], ...]`.

    Returns
    -------
    tuple
        - `length` (float):
            Length of minimal 2-dimensional bounding box.
        - `width` (float):
            Width of minimal 2-dimensional bounding box.
        - `center` (numpy.ndarray, type float):
            Center of 2-dimensional minimal bounding box in shape `[x, y]`.
        - `cornerpoints` (numpy.ndarray, type float):
            2-dimensional array of four cornerpoints of the minimal bounding box
            in shape `[[x0, y0], [x1, y1], [x2, y2], [x3, y3]]`.
    """
    contour_cv2 = measure_2d.utils._array_to_cv2contour(contour)
    min_bb_rect = cv2.minAreaRect(contour_cv2[0])

    # extract width, length and center from cv2 format
    (center_min_bb_y, center_min_bb_x), (length, width), _ = min_bb_rect
    center = np.array([center_min_bb_x, center_min_bb_y])

    # extract corner points from cv2 format
    box_cv2 = cv2.boxPoints(min_bb_rect)
    cornerpoints = np.zeros((4, 2))
    cornerpoints[:, 0] = box_cv2[:, 1]
    cornerpoints[:, 1] = box_cv2[:, 0]

    # if bounding box found: adjust borderline definition
    if length > 0 and width > 0:
        length += 1
        width += 1
        center += 0.5
        cornerpoints[1, 1] += 1
        cornerpoints[2, :] += 1
        cornerpoints[3, 0] += 1

    return length, width, center, cornerpoints


def area_equal_diameter(projection_area):
    """Calculate area-equal diameter.
    Parameters
    ----------
    projection_area : float
        Projection area.

    Returns
    -------
    float
        - `area_equal_diameter` (float):
            2D area-equal diameter.
    """
    return np.sqrt(4*projection_area/np.pi)


def perimeter_equal_diameter(perimeter):
    """Calculate perimeter-equal diameter.

    Parameters
    ----------
    perimeter : float
        Perimeter.

    Returns
    -------
    float
        - `perimeter_equal_diameter` (float):
            Perimeter-equal diameter.
    """
    return perimeter/np.pi


def max_inclosing_circle(bw):
    """Calculate maximum inclosing circle of an object.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `center` (numpy.ndarray, type float):
            Center position of maximum inclosing circle in shape `[x, y]`.
        - `diameter` (float):
            Diameter of maximum inclosing circle.
    """
    assert bw.ndim == 2, "Binary image must be 2-dimensional."

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")

    bw = np.pad(bw,
                pad_width=2,
                mode='constant',
                constant_values=False)

    distance_map = cv2.distanceTransform(bw.astype('uint8'),
                                         cv2.DIST_L2,
                                         cv2.DIST_MASK_PRECISE)

    radius = np.amax(distance_map)

    idx_max_distance = np.where(distance_map == radius)
    center = np.zeros((2, ))
    center[0] = idx_max_distance[0][0] - 1
    center[1] = idx_max_distance[1][0] - 1

    diameter = 2 * radius

    return center, diameter


def min_enclosing_circle(contour):
    """Calculate minimum enclosing circle of an object based on its list of coordinates.

    Parameters
    ----------
    contour : numpy.ndarray, type int
        Array of contour points in shape `[[x0, y0], [x1, y1], ...]`.

    Returns
    -------
    tuple
        - `center` (numpy.ndarray, type float): Center of minimum enclosing circle.
        - `diameter` (float): Diameter of minimum enclosing circle.
    """
    # transform coordinates to cv2 representation:
    coords_cv2 = np.zeros_like(contour)
    coords_cv2[:, 0] = contour[:, 1]
    coords_cv2[:, 1] = contour[:, 0]

    coords_cv2 = (coords_cv2.reshape((-1, 2, 1))).astype('int')

    # find min enclosing circle
    center_cv2, radius = cv2.minEnclosingCircle(coords_cv2)

    # convert to numpy array and transform to (x,y) coordinate system
    center = np.zeros((2,))
    center[0], center[1] = center_cv2[1], center_cv2[0]

    diameter = 2 * radius

    return center, diameter


def circumscribing_and_inscribing_circle(centroid, contour):
    """Calculate circumscribing and inscribing circle of an object shape [1].

    Parameters
    ----------
    centroid : numpy.ndarray, type float
        Centroid of object in shape `[x,y]`.
    contour : numpy.ndarray, type int
        Array of contour points in shape `[[x0, y0], [x1, y1], ...]`.

    Returns
    -------
    tuple
        - `diameter_circumscribing_circle` (float):
            Diameter of circumscribing circle.
        - `diameter_inscribing_circle` (float):
            Diameter of inscribing circle.

    References
    ----------
    [1] X. Li, Z. Wen, H. Zhu, Z. Guo and Y. Liu (2020). "An improved algorithm for
        evaluation of the minimum circumscribed circle and maximum inscribed circle
        based on the local minimax radius".
        In: The Review of scientific instruments 91(3), pp. 035103.
        DOI: https://doi.org/10.1063/5.0002233


    """
    assert centroid.ndim == 1
    assert contour.ndim == 2

    distances = spatial.distance.cdist(centroid.reshape((-1, 2)),
                                       contour,
                                       metric='euclidean')

    distances = distances.reshape((-1))
    radius_circumscribing_circle = max(distances)
    radius_inscribing_circle = min(distances)

    diameter_circumscribing_circle = 2 * radius_circumscribing_circle
    diameter_inscribing_circle = 2 * radius_inscribing_circle

    return diameter_circumscribing_circle, diameter_inscribing_circle


def geodeticlength_and_thickness(area, perimeter):
    """Calculate geodetic length and thickness based on area and
     diameter according to DIN ISO 9276-6.

    Parameters
    ----------
    area : float
        Projection area of shape.
    perimeter : float
        Perimeter of shape.

    Returns
    -------
    tuple
        - `geodeticlength` (float):
            Geodetic length of shape.
        - `thickness` (float):
            Thickness of shape.


    Notes:
    ------
    Calculation according to DIN ISO 9276-6:
    The geodetic lengths and thickness are approximated by an rectangle
    with the same area and perimeter:
    (1) `area = geodeticlength * thickness`
    (2) `perimeter = 2 * (geodetic_length + thickness)`
    """

    assert area >= 0, "`area` must be >= 0."
    assert perimeter >= 0, "`perimeter` must be >= 0."

    if area == 0:
        warnings.warn("`area` is zero.")
    
    if perimeter == 0:
        warnings.warn("`perimeter` is zero.")

    # White the help of Equation (1) we can rewrite Equation (2) to:
    # `geodetic_length**2 - 0.5 * perimeter * geodetic_length + area = 0`
    # Which we can solve with the pq-formula:
    # `geodetic_length = perimeter/4 +- sqrt((perimeter/4)**2 - area)`
    # since only the positive solution makes sense in our application

    # We will define a helping variable,
    # which describes the term under the square root:
    v = (perimeter/4)**2 - area

    # Make sure value under squareroot is > 0
    v = max(v, 0)

    # Calcuate geodetic_length with pq-formula (see above):
    geodetic_length = perimeter/4 + np.sqrt(v)

    # Calculate thickness by rewriting Equation (2):
    thickness = perimeter/2 - geodetic_length

    return geodetic_length, thickness


def max_2d_dimensions(max_chords, angles):
    """Calculates the max 2d dimensions of an object shape.
    `x_max` is the overall max chord of the object in all possible orientations.
    `y_max` is the longest chord orthogonal to `x_max` [1].

    Parameters
    ----------
    max_chords_2d : numpy.ndarray, type float
        1-dimensional array of max chords at different angles (`angles_2d`).
    angles_2d : numpy.ndarray, type float
        Respective angles to the `max_chords_2d` in ascending order.

    Returns
    -------
    tuple
        - `x_max` (float):
            Larger max dimension of object (definition see above).
        - `y_max` (float):
            Smaller max dimension of object (definition see above).

    References
    ----------
    [1] M. Steuer (2010). "Serial classification". In: AT Mineral Processing 51(1).
    """
    assert max_chords.shape == angles.shape, "max_chords and angles should have the same shape."

    if len(max_chords) == 0 or len(angles) == 0:
        warnings.warn("Input arrays are empty. Return (0, 0).")
        return 0, 0

    x_max = max_chords.max()
    idx_x_max = max_chords.argmax()
    angle_x_max = angles[idx_x_max]

    angle_y_max = (angle_x_max + 90) % 180
    idx_y_max = (np.abs(angles - angle_y_max)).argmin()
    y_max = max_chords[idx_y_max]

    return x_max, y_max


def convex_perimeter(bw_convex):
    """Calculate perimeter of 2D convex hull based on an binary image of convex hull.

    Parameters
    ----------
    bw_convex : numpy.ndarray, type bool
        2-dimensional binary convex image.

    Returns
    -------
    float
        - `convex_perimeter` (float):
            Convex perimeter.
    """
    assert bw_convex.dtype == 'bool', "`bw_convex` must be of dtype 'bool'."
    assert bw_convex.ndim == 2, "`bw_convex` must be 2-dimensional array"
    if np.count_nonzero(bw_convex.ravel()) == 0:
        warnings.warn("`bw_convex` is empty.")
        return 0

    labels = measure.label(bw_convex)
    props = measure.regionprops(labels)
    return props[0].perimeter
