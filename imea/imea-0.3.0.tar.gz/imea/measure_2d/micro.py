"""2-dimensional microdescriptors."""

import warnings

import numpy as np
from scipy import spatial, stats


def fractal_dimension_boxcounting(bw, pad_width=1):
    """Approximate fractal dimension by boxcounting method [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    pad_width : int, optional
        Width of applied zero-padding around the image, by default 1.

    Returns
    -------
    float
        - `fractal_dimension` (float):
            Approximated fractal dimension.


    References
    ----------
    [1] G.-B. So, H.-R. So, G.-G. Jin (2017): "Enhancement of the
        Box-Counting Algorithm for fractal dimension estimation".
        In: Pattern Recognition Letters, 98, pp. 53-58.
        https://doi.org/10.1016/j.patrec.2017.08.022

    """
    bw = np.pad(bw, pad_width=pad_width,
                mode='constant', constant_values=False)

    n_true_pixels = np.sum(bw.ravel())
    if n_true_pixels <= 1:
        # only a point --> fractal dimension is zero
        warnings.warn(
            '`bw` contains <= 1 true pixel: Fractal dimension is zero.')
        return 0
    else:
        number_of_boxes, box_sizes = _count_at_different_boxsizes(bw)

        if len(box_sizes) <= 1 or len(number_of_boxes) <= 1:
            # only a point --> fractal dimension is zero
            warnings.warn(
                '`bw` contains only a point: Fractal dimension is zero.')
            return 0
        else:
            return _approximate_fractal_dimension_by_slope(
                number_of_boxes, box_sizes)


def fractal_dimension_perimeter(contour, max_feret, n_stepsizes=10, step_size_min=2.0):
    """Approximate fractal dimension with perimeter method. [1]

    Parameters
    ----------
    contour : numpy.ndarray, type float
        Array of contourpoints in shape (n, 2)
        (e.g. `[[x0, y0], [x1, y1], [x2, y2], ...]`).
    max_feret : float
        Max feret diameter of object shape for norming the perimeters.
    n_stepsizes : int, optional
        Number of different stepsizes to take, by default 10
    step_size_min : float, optional
        Minimum stepsize, by default 2.0.

    Returns
    -------
    float
        - `fractal_dimension` (float):
            Approximated fractal dimension.

    Notes
    -----
    Stepsizes range from step_size_min to step_size_max in a log2 grid.
    step_size_max is set to 0.3 * max_feret according to DIN ISO 9276-6.

    References
    ----------
    [1] Deutsches Institut für Normung e. V. (2012). DIN ISO 9276-6 -
        Darstellung der Ergebnisse von Par-tikelgrößenanalysen:
        Teil 6: Deskriptive und quantitative Darstellung der Form
        und Morphologie von Partikeln.
    """
    # max stepsize is defined by [1] to:
    step_size_max = 0.3 * max_feret
    step_sizes = np.logspace(np.log2(step_size_min),
                             np.log2(step_size_max),
                             num=n_stepsizes,
                             endpoint=True,
                             base=2)

    perimeters = _uniformly_structured_gait(contour, step_sizes)

    if np.sum(perimeters) > 0:
        # Normalize by maximum feret diameter
        perimeters_normed = perimeters / max_feret
        return _approximate_fractal_dimension_by_slope(
            perimeters_normed,
            step_sizes)
    else:
        # only a point --> fractal dimension is zero
        warnings.warn(
            '`contour` represents only a point: Fractal dimension is zero.')
        return 0


def _count_at_different_boxsizes(bw, min_box_size=2):
    """Count number of non-zero and non-full boxes
    of binary image `bw` at different box sizes.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    min_box_size : int, optional
        Minimum investigated box size, by default 2
        `min_box_size` must be representable as `2**n, where
        `n` is a natural number.

    Returns
    -------
    tuple
        - `number_of_boxes` (numpy.ndarray, type int):
            Number of found non-zero and non-full boxes
            for the corresponding box size.
        - `box_sizes` (np.darray, type int):
            Array of corresponding box sizes.
    """
    assert bw.ndim == 2, "Binary image must be 2-dimensional."

    bw_pad = _zeropad_bw_to_shape_of_power_two(bw)

    # min and max investigated box size
    max_box_size = bw_pad.shape[0] / 2
    exp_max_box = int(np.log2(max_box_size))
    exp_min_box = int(np.log2(min_box_size))

    # array of investigated box sizes
    n_steps = exp_max_box - exp_min_box + 1
    box_sizes = np.logspace(exp_min_box, exp_max_box,
                            num=n_steps, base=2, dtype='int', endpoint=True)

    # initialize array for solutions
    number_of_boxes = np.zeros(box_sizes.shape, dtype='int')

    # determine number of boxes for different box sizes
    for i, box_size in enumerate(box_sizes):
        number_of_boxes[i] = _count_nonfull_nonzero_boxes(bw_pad, box_size)

    return number_of_boxes, box_sizes


def _count_nonfull_nonzero_boxes(bw, box_size):
    """Calculate number of boxes of shape (`box_size`, `box_size`)
    that are non-empty and non-full in an binary image.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    box_size : int
        Investigated box size.

    Returns
    -------
    int
        - `n_boxes` (int)
            Number of found non-empty and non-full boxes.
    """
    # create boxes of shape (box_size,box_size) and store results in a matrix
    # an efficient implementation of this procedere is given by
    # [https://github.com/rougier/numpy-100 (#87)]
    # cited from [https://gist.github.com/viveksck/1110dfca01e4ec2c608515f0d5a5b1d1]:
    S = np.add.reduceat(np.add.reduceat(bw, np.arange(0, bw.shape[0], box_size), axis=0),
                        np.arange(0, bw.shape[1], box_size),
                        axis=1)

    # count non-empty (0) and non-full boxes (box_sizes*box_size)
    return len(np.where((S > 0) & (S < box_size * box_size))[0])


def _uniformly_structured_gait(contour, step_sizes):
    """Perform uniformly structured gait at different `step_sizes` and return walked perimeters.

    Parameters
    ----------
    contour : numpy.ndarray, type float
        Array of contourpoints in shape (N, 2)
        (e.g. `[[x0, y0], [x1, y1], [x2, y2], ...]`).
    step_sizes : numpy.ndarray, type float
         1-dimensional array of the different step sizes to walk.

    Returns
    -------
    numpy.ndarray, type float
        - `perimeters` (numpy.ndarray, type float)
            Array of walked perimeter per step size.
    """
    # initialize parameters
    perimeters = np.zeros(step_sizes.shape)

    # walk around contour with different stepsizes
    for j, step_size in enumerate(step_sizes):
        walked_distances = []
        start_point = contour[0]
        i = 0

        while i < len(contour) - 1:
            # choose next point as endpoint
            i += 1
            end_point = contour[i]

            # check if point is more away than stepsize
            distance = spatial.distance.euclidean(start_point, end_point)
            if distance >= step_size:
                # valid step --> save walked distance
                walked_distances.append(distance)
                # current point becomes now our next start point
                start_point = contour[i]
            else:
                pass

        perimeters[j] = sum(walked_distances)

    return perimeters


def _approximate_fractal_dimension_by_slope(measurements, step_sizes):
    """Approximate fractal dimension based on measurements and `step_sizes`
        by slope in the log/log Richardson plot [1].

    Parameters
    ----------
    measurements : numpy.ndarray, type float
        Array of measured length at different `step_sizes`.
    step_sizes : numpy.ndarray, type float
        Corresponding step_sizes.

    Returns
    -------
    float
        - `fractal_dimension` (float):
            Approximated fractal dimension.

    Notes
    -----
    Slope is approximate by linear regression of the curve in the log/log Richardson plot.

    References
    ----------
    [1] Deutsches Institut für Normung e. V. (2012). DIN ISO 9276-6 -
        Darstellung der Ergebnisse von Par-tikelgrößenanalysen:
        Teil 6: Deskriptive und quantitative Darstellung der Form
        und Morphologie von Partikeln.
    """
    assert measurements.shape == step_sizes.shape, "Measurements and stepsize must have same shape."

    # remove entries where measurements are zero
    measurements_org = measurements.copy()
    measurements = measurements[measurements_org != 0]
    step_sizes = step_sizes[measurements_org != 0]

    # Slope in richardson plot
    measurements_log2 = np.log2(measurements)
    step_sizes_log2 = np.log2(step_sizes)

    slope, _, _, _, _ = stats.linregress(
        step_sizes_log2, measurements_log2)

    if slope == 0:
        warnings.warn(
            "Slope is zero slope --> fractal dimension will be set to zero.")
        return 0
    else:
        return 1 - slope


def _zeropad_bw_to_shape_of_power_two(bw):
    """Transform binary image `bw` into shape ``(2**n, 2**n)``
    (where ``n`` is a natural number) by placing it on
        a black background.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.

    Returns
    -------
    numpy.ndarray, type bool
        - `bw_pad` (numpy.ndarray, type bool):
            Padded 2-dimensional binary image
            of shape `(2**n, 2**n)`, where `n` is a natural number.
    """
    # determine shape of the padded image
    max_img_size = max(bw.shape)
    exponent_bw_shape = int(np.ceil(np.log2(max_img_size)))
    padded_bw_size = 2**exponent_bw_shape
    padded_bw_shape = (padded_bw_size, padded_bw_size)

    # initialize padded image
    bw_pad = np.zeros(padded_bw_shape, dtype='bool')

    # determine shift, s. t. bw is inserted in the center of bw_pad
    shift_x = int((padded_bw_size - bw.shape[0]) / 2)
    shift_y = int((padded_bw_size - bw.shape[1]) / 2)

    # insert bw
    bw_pad[shift_x:bw.shape[0]+shift_x, shift_y:bw.shape[1]+shift_y] = bw

    return bw_pad
