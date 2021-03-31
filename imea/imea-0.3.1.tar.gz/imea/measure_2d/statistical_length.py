"""2-dimensional statistical length."""

import warnings

import numpy as np
from scipy import stats
from skimage import transform


def compute_statistical_lengths(bw, daplha=9):
    """Calculate statistical length distributions by rotating binary image `bw` in `dalpha` steps [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    daplha : number
        Rotation stepsize in degrees (0 - 180°), by default 9.

    Returns
    -------
    tuple
        - `feret_diameters` (numpy.ndarray, type int):
            1-dimensional array of Feret diameters for each rotation angle [1].
        - `martin_diameters` (numpy.ndarray, type int):
            1-dimensional array of Martin diameters for each rotation [1].
        - `nassenstein_diameters` (numpy.ndarray, type int):
            1-dimensional array of Nassenstein diameters for each rotation.
        - `max_chords` (numpy.ndarray, type int):
            1-dimensional array of maximum chord for each rotation [1].
        - `all_chords` (numpy.ndarray, type int):
            1-dimensional array of all chords for each rotation [1].
        - `angles` (numpy.ndarray, type float):
            1-dimensional array of measured angles in degree
            as determinated by `daplha`.

    References
    ----------
    [1] M. Pahl, G. Schädel und H. Rumpf (1973a). "Zusammenstellung von
        Teilchenformbeschreibungsmethoden: 1. Teil".
        In: Aufbereitungstechnik, 14(5), pp. 257–264.
    """

    assert daplha > 0, "`daplha` must be > 0°"
    assert daplha < 180, "`daplha` must be < 180°"

    angles = np.arange(0, 180, daplha)

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")

    feret_diameters = np.zeros(angles.shape, dtype='int')
    martin_diameters = np.zeros(angles.shape, dtype='int')
    nassenstein_diameters = np.zeros(angles.shape, dtype='int')
    max_chords = np.zeros(angles.shape, dtype='int')
    all_chords = np.array([])

    for i, angle in enumerate(angles):
        bw_rotated = transform.rotate(bw, angle, resize=True)
        # important: skimage.transform.rotate returns a greyscale image with values between 0 and 1
        # --> use simple thresholding to transform back to binary image
        bw_rotated = bw_rotated > 0.5

        feret_diameters[i], _ = feret(bw_rotated)

        martin_diameters[i], _ = martin(bw_rotated)

        nassenstein_diameters[i], _ = nassenstein(bw_rotated)

        all_chords_i, all_edgepoints_i = find_all_chords(bw_rotated)
        all_chords = np.append(all_chords, all_chords_i)

        max_chords[i], _ = _max_chord_from_all_chords(
            all_chords_i, all_edgepoints_i)

    return feret_diameters, martin_diameters, nassenstein_diameters, max_chords, all_chords, angles


def nassenstein(bw):
    """Calculates the Nassenstein diameter of an object shape [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `nassenstein_diameter` (int):
            Nassenstein diameter.
        - `idx` (numpy.ndarray, type int):
            Indexes of the start (0) and endpoint (1) of the Nassenstein diameter
            in shape `[[x0,y0], [x1,y1]]`.

    References
    ----------
    [1] M. Pahl, G. Schädel und H. Rumpf (1973a). "Zusammenstellung von
        Teilchenformbeschreibungsmethoden: 1. Teil".
        In: Aufbereitungstechnik, 14(5), pp. 257–264.

    Notes
    -----
    There might be several touching points in the lowest row.
        In this implementation we will evaluate the Nassenstein Durchmesser at the middle
        of the first continuous contact surface from left.

    """
    assert bw.dtype == 'bool', "`bw` should be boolean"
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")
        return 0, np.array([])

    bw_pad = np.pad(bw, pad_width=1, mode='constant', constant_values=False)

    # find lowest row
    n_true_pixels_y = np.count_nonzero(bw_pad, axis=1)
    n_true_pixels_y = n_true_pixels_y[::-1]  # we count from bottom
    first_touching_point = _first_nonzero(n_true_pixels_y, axis=0)

    if first_touching_point == -1:
        warnings.warn("No object found.")
        return 0, np.array([])

    n_pixels_x = bw_pad.shape[0]
    idx_lowest_row = n_pixels_x - first_touching_point - 1
    lowest_row = bw_pad[idx_lowest_row, :]

    # Get evaluation column:
    # There might be several touching points (see Notes)
    # --> we will evaluate at center of first continuous contact surface from left

    changing_points_row = np.where(lowest_row[:-1] != lowest_row[1:])[0]
    changing_points_row = np.sort(changing_points_row)

    start_idx_first_contact = changing_points_row[0]
    end_idx_first_contact = changing_points_row[1]

    # column, we want to evaluate
    # Note: np.ceil is essential: If we only have one touching point
    # (e.g. at index 3 and 4) then we need to round up to 4, to extract
    # the correct column (refers to the definition of changing idx from above)
    evaluation_idx = int(
        np.ceil((start_idx_first_contact + end_idx_first_contact)/2))

    # extract the column at evaluation idx:
    nassenstein_column = bw_pad[:, evaluation_idx]

    # we measure starting from bottom
    nassenstein_column = nassenstein_column[::-1]
    # again we consider the changing points to determine the Nassenstein diameter
    changing_idx_nassenstein_column = np.where(
        nassenstein_column[:-1] != nassenstein_column[1:])[0]
    changing_idx_nassenstein_column = np.sort(changing_idx_nassenstein_column)

    # since we started counting from bottom,
    # we have to transform the indexes to the coordinate system from top
    measurement_point_bottom = n_pixels_x - changing_idx_nassenstein_column[0]
    measurement_point_top = n_pixels_x - changing_idx_nassenstein_column[1]

    nassenstein_diameter = measurement_point_bottom - measurement_point_top

    # get indexes and undo padding shift
    idx = np.zeros((2, 2), dtype=('int'))
    idx[0, 0], idx[0, 1] = measurement_point_top - 2, evaluation_idx
    idx[1, 0], idx[1, 1] = measurement_point_bottom - 2, evaluation_idx

    return nassenstein_diameter, idx


def feret(bw):
    """Calculate Feret diameter of an object (orthogonal to y-direction) [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `feret_diameter` (int):
            2D Feret diameter.
        - `idx_x` (numpy.ndarray, type int):
            x-coordinates of the two Feret calipers in shape
            `[x0, x1]`.

    References
    ----------
    [1] M. Pahl, G. Schädel und H. Rumpf (1973a). "Zusammenstellung von
        Teilchenformbeschreibungsmethoden: 1. Teil".
        In: Aufbereitungstechnik, 14(5), pp. 257–264.
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")
        return 0, np.array([])

    n_pixels_x = bw.shape[0]

    # "squeeze" bw in y-direction into one column
    n_true_pixels_y = np.count_nonzero(bw, axis=1)

    # caliper from top
    idx_x_first_nonzero = _first_nonzero(n_true_pixels_y, axis=0)
    if idx_x_first_nonzero == -1:
        # no element found
        return 0, np.array([])

    # caliper from bottom
    n_true_pixels_y_reversed = n_true_pixels_y[::-1]
    idx_first_nonzero_from_bottom = _first_nonzero(
        n_true_pixels_y_reversed, axis=0)
    idx_x_last_nonzero = n_pixels_x - idx_first_nonzero_from_bottom

    # feret diameter
    feret_diameter = idx_x_last_nonzero - idx_x_first_nonzero
    idx_x = np.array([idx_x_first_nonzero, idx_x_last_nonzero])

    return feret_diameter, idx_x


def martin(bw, area_share_from_bottom=0.5):
    """Calculate Martin diameter of an object (in y-direction) [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    area_share_from_bottom : float, optional
        Area share, where the Martin diameter is measured,
        by default 0.5 (original definition of the Martin diameter.)

    Returns
    -------
    tuple
        - `martin_diameter` (int):
            Martin diameter.
        - `idx` (numpy.ndarray, type int):
            Indexes of the start (0) and endpoint (1)
            of the Martin diameter in shape `[[x0,y0], [x1,y1]]`.

    References
    ----------
    [1] M. Pahl, G. Schädel und H. Rumpf (1973a). "Zusammenstellung von
        Teilchenformbeschreibungsmethoden: 1. Teil".
        In: Aufbereitungstechnik, 14(5), pp. 257–264.

    Notes
    -----
    The original Martin diameter is is measured at the x-position,
    where the object is split into 50% / 50% area share.
    However, we can also calculate a diameter at a flexible area share.
    This is given by `area_share_from_bottom`:
    `area_share_from_bottom = 1 - area_share_from_top`
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"
    assert (area_share_from_bottom >= 0 and
            area_share_from_bottom <= 1), "Area share must be in interval [0, 1]."

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")
        return 0, np.array([])

    if area_share_from_bottom == 0 or area_share_from_bottom == 1:
        warnings.warn("Return 0 since area share = {:0.1f}".format(
            area_share_from_bottom))
        return 0, np.array([])

    area_share_from_top = 1 - area_share_from_bottom

    n_true_pixels_y = np.count_nonzero(bw, axis=1)

    # get the index where the area_share is reached (from top)
    cum_area = np.cumsum(n_true_pixels_y)
    area = cum_area[-1]
    if area == 0:
        warnings.warn("`bw` does not contain any objects. Return 0.")
        return 0, np.array([])

    area_threshold = area_share_from_top * area
    idx_x_split = (cum_area > area_threshold).argmax()

    # extract row of this position
    split_row = bw[idx_x_split, :]

    # calculate the martin diameter of this dimension
    n_pixels = split_row.shape[0]

    idx_y_first_nonzero = split_row.argmax()
    row_split_reversed = split_row[::-1]
    idx_y_last_nonzero = n_pixels - row_split_reversed.argmax()

    martin_diameter = idx_y_last_nonzero - idx_y_first_nonzero

    idx = np.array([
                   [idx_x_split, idx_y_first_nonzero],
                   [idx_x_split, idx_y_last_nonzero]
                   ])

    return martin_diameter, idx


def find_all_chords(bw):
    """Calculate chords of an object shape in y-direction [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `all_chords` (numpy.ndarray, type int):
            1-dimensional array of found chords `c` in shape `[c0, c1, ...]`.
        - `all_edgepoints` (numpy.ndarray, type int):
            2-dimensional array of edgepoints corresponding to `all_chords`
            in shape `[[x0a, y0a], [x0b, y0b], [x1a, y1a], [x1b, y1b], ...]`,
            where `a` is the start and `b` is the endpoint of the corresponding edge
            and `0, 1, ...` the index of the corresponing chords.

    References
    ----------
    [1] M. Pahl, G. Schädel und H. Rumpf (1973a). "Zusammenstellung von
        Teilchenformbeschreibungsmethoden: 1. Teil".
        In: Aufbereitungstechnik, 14(5), pp. 257–264.
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")
        return np.array([]), np.array([])

    all_chords = np.array([], dtype='int')
    all_edgepoints = np.zeros((0, 2), dtype='int')

    bw_pad = np.pad(bw, pad_width=1, mode='constant', constant_values=False)

    # find changing points in y-direction
    bw_rep = np.repeat(bw_pad, repeats=1, axis=1)
    idx_with_changes = np.array(
        np.where(bw_rep[:, :-1] != bw_rep[:, 1:]))

    idx_x = idx_with_changes[0, :]
    idx_y = idx_with_changes[1, :]
    changing_points = np.column_stack((idx_x, idx_y))

    # we only need to go through rows, where changes accur:
    for u in np.unique(idx_x):
        # extract points of this row
        points_i = changing_points[np.where(changing_points[:, 0] == u)]

        # to calculate the chords we now need to determine the distance
        # between pairs of changingpoints in y-direction
        y_coords_i = points_i[:, 1]

        # since the leftest row is always filled with false pixels (see padding above),
        # we know that the first pointwill be a changing point from False to True
        # and the next point then will be a changing point from True to False.
        # More generally: If we sort the y-coordinates of all changing-points in ascending order
        # and indexes start at zero, then the following applies:
        # All changing points with even indexes (0, 2, ...) are starting points
        # and all ending points with uneven indexes (1, 3, ...) are ending points

        # as promised: sort y_coordinates in ascending order
        y_coords_i_sorted = np.sort(y_coords_i)

        # starting points have even indexes
        start_points_i = y_coords_i_sorted[0::2]

        # ending points have uneven indexes
        end_points_i = y_coords_i_sorted[1::2]

        # The choords are the distance between the corresponding starting and ending points
        chords_i = end_points_i - start_points_i

        # add found choords to result list
        all_chords = np.append(all_chords, chords_i)

        # undo padding for determinating idx
        points_i = points_i - 1

        all_edgepoints = np.concatenate(
            (all_edgepoints, points_i))

    return all_chords, all_edgepoints


def find_max_chord(bw):
    """Calculate the maximum chords of an object shape in y-direction [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    tuple
        - `max_chord` (int):
            Maximum chord in y-direction.
        - `idx` (numpy.ndarray, type int):
            Start (0) and endpoint (1) of max chord in shape `[[x0, y0], [x0, y0]]`.

    References
    ----------
    [1] M. Pahl, G. Schädel und H. Rumpf (1973a). "Zusammenstellung von
        Teilchenformbeschreibungsmethoden: 1. Teil".
        In: Aufbereitungstechnik, 14(5), pp. 257–264.
    """
    assert bw.dtype == 'bool', "`bw` must be of dtype 'bool'."
    assert bw.ndim == 2, "`bw` must be 2-dimensional array"

    if np.count_nonzero(bw) == 0:
        warnings.warn("`bw` is empty.")
        return 0, np.array([])

    all_chords, all_edgepoints = find_all_chords(bw)
    max_chord, idx = _max_chord_from_all_chords(
        all_chords, all_edgepoints)

    return max_chord, idx


def distribution_parameters(distribution):
    """Calculate distribution parameters of an array.

    Parameters
    ----------
    distribution : numpy.ndarray, type float
        An array.

    Returns
    -------
    tuple
        - `max_value` (float):
            Max value in `distribution`.
        - `min_value` (float):
            Min value in `distribution`.
        - `median_value` (float):
            Median value in `distribution`.
        - `mean_value` (float):
            Mean value in `distribution`.
        - `mode` (float):
            Mode value in `distribution`.
        - `std` (float):
            Standard deviation of `distribution`.
    """
    distribution = distribution.ravel()

    if len(distribution) == 0:
        warnings.warn("`distribution` is empty --> return None.")
        return None, None, None, None, None, None
    max_value = distribution.max()
    min_value = distribution.min()
    median_value = np.median(distribution)
    mean_value = np.median(distribution)
    modes, _ = stats.mode(distribution)
    mode = modes[0]
    std = np.std(distribution)

    return max_value, min_value, median_value, mean_value, mode, std


def _max_chord_from_all_chords(all_chords, all_edgepoints):
    """Determine the maximum of all chords.

    Parameters
    ----------
    all_chords : numpy.ndarray, type int
        1-dimensional array of found chords `c` in shape `[c0, c1, ...]`.
    all_edgepoints : numpy.ndarray, type int
        2-dimensional array of edgepoints corresponding to `all_chords`
        in shape `[[x0a, y0a], [x0b, y0b], [x1a, y1a], [x1b, y1b], ...]`,
        where `a` is the start and `b` is the endpoint of the corresponding edge
        and `0, 1, ...` the index of the corresponing chords.

    Returns
    -------
    tuple
        - `max_chord` (int):
            Maximum chord.
        - `idx_max_chord` (numpy.ndarray, type int):
            Start (0) and endpoint (1) of max chord in shape `[[x0,y0],[x1,y1]]`.
    """
    if len(all_chords) == 0:
        warnings.warn("No chords passed. Return 0.")
        return 0, np.array([])

    max_chord = all_chords.max()
    idx = all_chords.argmax()
    idx_points = 2 * idx

    idx_max_chord = all_edgepoints[idx_points:idx_points+2, :]

    # make borderline definition consistent
    idx_max_chord[:, 1] = idx_max_chord[:, 1] + 1

    return max_chord, idx_max_chord


def _first_nonzero(array, axis, invalid_val=-1):
    """Calculate index of first nonzero entry of `arr` along `axis.

    Parameters
    ----------
    array : numpy.ndarray
        Array.
    axis : int
        Axis along which is measured.
    invalid_val : int, optional
        Value that is returned,
        if no nonzero-entry is found, by default -1.

    Returns
    -------
    int
        - `first_nonzero_idx` (int):
            Index of first nonzero entry of `array` along `axis`.
    """
    assert axis <= array.ndim, "`axis` must be within ndim of array."

    mask = (array != 0)
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)
