"""**imea** core functions to extract 2D and/or 3D shape measurements from images."""

import warnings

import numpy as np
import pandas as pd
from skimage import measure

from imea import measure_2d, measure_3d, tools


def shape_measurements_3d(img_3d, threshold_mm, spatial_resolution_xy,
                          spatial_resolution_z, dalpha=9,
                          min_object_area=10, n_objects_max=-1):
    """Extract 2D and 3D rotation and translation invariant shape measurements
        from a 3d grayscale image.

    Parameters
    ----------
    img_3d : numpy.ndarray, type float
        3d image in grayscale representation
        (background is zero, grayvalues represent height).
    threshold_mm : float
        Threshold in millimeters for segmentation of `img_3d`.
        Pixels <= `threshold` are considered as background,
        pixels > `threshold_mm` as object (foreground).
    spatial_resolution_xy : float
        Spatial resolution of `img_3d` in x and y direction in [mm/pixel].
        Assumes image is already calibrated, i.e. dx = dy, see Notes.
    spatial_resolution_z : float
        Spatial resolution of `img_3d` in z-direction (height) in [mm/grayvalue].
    dalpha : float, optional
        Angle in degrees by which object is rotated at each iteration,
        (e. g. for statistical length), by default 9.
    min_object_area : int, optional
        Minimum area in pixels of a region to be considered as an object, by default 10.
    n_objects_max : int, optional
        Maximum number of objects to be extracted.
        If `n_objects_max=-1`, then all objects are extracted, by default -1.

    Returns
    -------
    tuple
        - `df_2d` (pandas.DataFrame):
            Pandas dataframe including all 2D shape measurements currently supported by **imea**
            objects are represented row-wise, shape measurements area returned column-wise.
        - `df_3d` (pandas.DataFrame):
            Pandas dataframe including all 3D shape measurements currently supported by **imea**
            objects are represented row-wise, shape measurements area returned column-wise.

    Notes
    -----
    You might want to use `skimage.transform.rescale` before calling this function
    if your image is not already calibrated, i. e. dx != dy.
    """
    assert type(img_3d) == np.ndarray,\
        "`img_3d` should be an numpy.ndarray"
    assert img_3d.ndim == 2,\
        "`img_3d` should be 2D array"
    assert img_3d.dtype != 'bool',\
        "`img_3d` is a boolean not numeric array.\
         Please use `imea.extract_shape_measurements_2d()` for 2D shape measurements"
    assert spatial_resolution_xy > 0,\
        "`spatial_resolution_xy` must be > 0 mm/Pixel."
    assert spatial_resolution_z > 0,\
        "`spatial_resolution_z` must be > 0 mm/grayvalue."

    threshold_gv = threshold_mm / spatial_resolution_z

    imgs_3d, bws = tools.preprocess.extract_and_preprocess_3d_imgs(img_3d,
                                                                   threshold_gv,
                                                                   min_object_area,
                                                                   n_objects_max)
    df_3d = []
    df_2d = []

    for (img_3d, bw) in zip(imgs_3d, bws):
        # 3D shape measurements
        df_3d_i = _shape_measurements_3d_single_object(img_3d,
                                                       spatial_resolution_xy,
                                                       spatial_resolution_z,
                                                       dalpha)
        df_3d.append(df_3d_i)

        # 2D shape measurements
        df_2d_i, _, _ = _shape_measurements_2d_single_object(bw,
                                                             spatial_resolution_xy,
                                                             dalpha)
        df_2d.append(df_2d_i)

    df_3d = pd.DataFrame(df_3d)
    df_2d = pd.DataFrame(df_2d)

    return df_2d, df_3d


def shape_measurements_2d(bw, spatial_resolution_xy=1, dalpha=9,
                          return_statistical_lengths=False, return_all_chords=False):
    """Extract 2D rotation and translation invariant shape measurements
        from a binary image.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    spatial_resolution_xy : float, optional
        Spatial resolution of image in [mm/pixel] to return values in metric values [mm].
        If `spatial_resolution_xy` is 1 measurements are returned in [pixels],
        by default 1.
    dalpha : int, optional
        Angle in degrees [°] to rotate `bw` at each iteration.
        Should be a fraction of 180° (180°/`n`), where `n`
        is a natural number, by default 9.
    return_statistical_lengths : bool, optional
        If True, original statistical lengths distributions are returned,
        by default False.
    return_all_chords : bool, optional
        If True, an array with all found chords are returned,
        by default False.

    Returns
    -------
    tuple
        - `df_2d` (pandas.DataFrame):
            Pandas dataframe including all 2D shape measurements currently supported by **imea**
            objects are represented row-wise, shape measurements area returned column-wise.
        - `statistical_lengths` (list, optional):
            List of `n` `pandas.DataFrame`s, where each dataframe includes
            statistical lengths (columns) for all iterated angles (`0° : dalpha : 180°`).
            Only provided if `return_statistical_lengths` is True.
        - `all_chords` (numpy.ndarray, optional):
            1-dimensional array with all found chords for all angles.
            Only provided if `return_all_chords` is True.
    """
    assert type(bw) == np.ndarray, "`bw` must be an numpy.ndarray"
    assert bw.ndim == 2, "`bw` must be 2D array"
    assert bw.dtype == 'bool', "`bw` must be binary image"

    assert spatial_resolution_xy > 0, "`spatial_resolution_xy` must be > 0."
    assert dalpha > 0, "`dalpha` must be > 0."
    assert dalpha < 180, "`dalpha` must be < 180°."

    all_chords = np.array([])
    df_2d = []
    statistical_lengths = []

    labels, n_objects = measure.label(bw, return_num=True)

    if n_objects > 0:
        for i in range(1, n_objects+1):
            bw_single = np.zeros_like(bw)
            bw_single[labels == i] = True

            shape_measurements_i, statistical_lengths_i, \
                all_chords_i = _shape_measurements_2d_single_object(bw_single,
                                                                    spatial_resolution_xy,
                                                                    dalpha)

            df_2d.append(shape_measurements_i)
            statistical_lengths.append(statistical_lengths_i)
            all_chords = np.append(all_chords, all_chords_i)
    else:
        warnings.warn("`bw` does not contain any objects.")

    df_2d = pd.DataFrame(df_2d)

    # Return depending on settings
    if not return_statistical_lengths and not return_all_chords:
        return df_2d
    elif return_statistical_lengths and not return_all_chords:
        return df_2d, statistical_lengths
    elif not return_statistical_lengths and return_all_chords:
        return df_2d, all_chords
    else:
        return df_2d, statistical_lengths, all_chords


def _shape_measurements_3d_single_object(img_3d, spatial_resolution_xy,
                                         spatial_resolution_z, dalpha):
    """Extract 3D rotation and translation invariant shape measurements
    from a 3d image (represented as grayscale) containing one object.

    Parameters
    ----------
    img_3d : numpy.ndarray, type float
        2-dimensional grayscale heightmap of single object with equal spacing, i.e. dx = dy = dz.
        Pixels not showing the pixel should be 0.
    spatial_resolution_xy : float
        Spatial resolution of `img_3d` in x and y-direction in [mm/pixel]
    spatial_resolution_z : float
        Spatial resolution of img_3d in z-direction (height) in [mm/grayvalue].
    dalpha : float
        Angle in degrees by which object is rotated at each iteration,
        (e. g. for Feret diameter).

    Returns
    -------
    dict
        - `df_3d` (dict):
            3D shape measurements.

    Notes
    -----
        Assumes only one object per binary image
        (multiple objects are handeled by higher order functions).
    """

    img_3d_equalspace, spatial_resolution = tools.preprocess.equalspace_3d_img(
        img_3d, spatial_resolution_xy, spatial_resolution_z)
    convex_hull = measure_3d.utils.compute_convexhull(img_3d_equalspace)

    volume = measure_3d.macro.volume(img_3d_equalspace, spatial_resolution)
    volume_convexhull = measure_3d.macro.volume_convexhull(convex_hull,
                                                           spatial_resolution)
    surface_area = measure_3d.macro.surfacearea_convexhull(convex_hull,
                                                           spatial_resolution)

    diameter_volume_equivalent = measure_3d.macro.volume_equivalent_diameter(
        volume)
    diameter_surfacearea_equivalent = measure_3d.macro.surfacearea_equivalent_diameter(
        surface_area)

    width_3d_bb, length_3d_bb, height_3d_bb = measure_3d.macro.min_3d_bounding_box(
        img_3d_equalspace, spatial_resolution)

    feret_3d_max, feret_3d_min, x_max_3d,\
        y_max_3d, z_max_3d = measure_3d.macro.feret_and_max_dimensions_3d(convex_hull,
                                                                          spatial_resolution,
                                                                          dalpha)

    df_3d = {
        "volume": volume,
        "volume_convexhull": volume_convexhull,
        "surface_area": surface_area,
        "diameter_volume_equivalent": diameter_volume_equivalent,
        "diameter_surfacearea_equivalent": diameter_surfacearea_equivalent,
        "width_3d_bb": width_3d_bb,
        "length_3d_bb": length_3d_bb,
        "height_3d_bb": height_3d_bb,
        "feret_3d_max": feret_3d_max,
        "feret_3d_min": feret_3d_min,
        "x_max_3d": x_max_3d,
        "y_max_3d": y_max_3d,
        "z_max_3d": z_max_3d
    }

    return df_3d


def _shape_measurements_2d_single_object(bw, spatial_resolution_xy, dalpha):
    """Extract 2D rotation and translation invariant shape measurements
    of a binary image containing one object.

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    spatial_resolution_xy : float
        Spatial resolution of image in [mm/pixel].
    dalpha : int
        Angle in degrees [°] to rotate `bw` at each iteration.
        Should be a fraction of 180° (180°/`n`), where `n`
        is a natural number.

    Returns
    -------
    tuple
        - `df_2d` (pandas.DataFrame):
            Pandas dataframe with one column for each shape measurement.
        - `statistical_lengths` (pandas.DataFrame):
            Pandas dataframe of statistical lengths measured
            at each rotation angle.
        - `all_chords` (numpy.ndarray, type float):
            Array of all found choords for all rotation angles.

    Notes
    -----
        Assumes only one object per binary image
        (multiple objects are handeled by higher order functions).
    """
    # Shape measurements available in skimage
    perimeter, area_projection, area_filled, area_convex, major_axis_length, \
        minor_axis_length, centroid, coords, bw_cropped, \
        bw_convex = measure_2d.utils.skimage_measurements(bw)

    # Contour for further processing
    contour = measure_2d.utils.find_contour(bw_cropped)

    # Circles
    _, diameter_max_inclosing_circle = measure_2d.macro.max_inclosing_circle(
        bw)
    _, diameter_min_enclosing_circle = measure_2d.macro.min_enclosing_circle(
        contour)

    diameter_circumscribing_circle, diameter_inscribing_circle \
        = measure_2d.macro.circumscribing_and_inscribing_circle(
            centroid, contour)

    # Statistical lengths
    feret_diameters, martin_diameters, nassenstein_diameters, maxchords, allchords,\
        measured_angles = measure_2d.statistical_length.compute_statistical_lengths(
            bw_cropped, daplha=dalpha)

    feret_max, feret_min, feret_median, feret_mean, \
        feret_mode, feret_std = measure_2d.statistical_length.distribution_parameters(
            feret_diameters)

    martin_max, martin_min, martin_median, martin_mean, \
        martin_mode, martin_std = measure_2d.statistical_length.distribution_parameters(
            martin_diameters)

    nassenstein_max, nassenstein_min, nassenstein_median, nassenstein_mean, \
        nassenstein_mode, nassenstein_std = measure_2d.statistical_length.distribution_parameters(
            nassenstein_diameters)

    maxchords_max, maxchords_min, maxchords_median, maxchords_mean, \
        maxchords_mode, maxchords_std = measure_2d.statistical_length.distribution_parameters(
            maxchords)

    allchords_max, allchords_min, allchords_median, allchords_mean, \
        allchords_mode, allchords_std = measure_2d.statistical_length.distribution_parameters(
            allchords)

    # Main and maximum dimensions
    x_max, y_max = measure_2d.macro.max_2d_dimensions(
        maxchords, measured_angles)
    width_min_bb, length_min_bb, _, _ = measure_2d.macro.min_2d_bounding_box(
        bw_cropped)

    # Equal diameters
    diameter_equal_area = measure_2d.macro.area_equal_diameter(area_projection)
    diameter_equal_perimeter = measure_2d.macro.perimeter_equal_diameter(
        perimeter)

    # Geodatic length and thickness
    geodeticlength, thickness = measure_2d.macro.geodeticlength_and_thickness(
        area_projection, perimeter)

    # Convex perimeter
    convex_perimeter = measure_2d.macro.convex_perimeter(bw_convex)

    # Measurements based on erosion
    n_erosions = measure_2d.meso.erosions_till_erase(
        bw_cropped)
    n_erosions_complement = measure_2d.meso.erosions_till_erase_complement(
        bw_cropped, bw_convex)

    # Fractal dimension
    fractal_dimension_boxcounting_method = measure_2d.micro.fractal_dimension_boxcounting(
        bw_cropped)
    fractal_dimension_perimeter_method = measure_2d.micro.fractal_dimension_perimeter(
        contour, feret_max)

    df_2d = {
        "perimeter": perimeter * spatial_resolution_xy,
        "convex_perimeter": convex_perimeter * spatial_resolution_xy,
        "area_projection": area_projection * spatial_resolution_xy**2,
        "area_filled": area_filled * spatial_resolution_xy**2,
        "area_convex": area_convex * spatial_resolution_xy**2,
        "major_axis_length": major_axis_length * spatial_resolution_xy,
        "minor_axis_length": minor_axis_length * spatial_resolution_xy,
        "diameter_max_inclosing_circle": diameter_max_inclosing_circle * spatial_resolution_xy,
        "diameter_min_enclosing_circle": diameter_min_enclosing_circle * spatial_resolution_xy,
        "diameter_circumscribing_circle": diameter_circumscribing_circle * spatial_resolution_xy,
        "diameter_inscribing_circle": diameter_inscribing_circle * spatial_resolution_xy,
        "diameter_equal_area": diameter_equal_area * spatial_resolution_xy,
        "diameter_equal_perimeter": diameter_equal_perimeter * spatial_resolution_xy,
        "x_max": x_max * spatial_resolution_xy,
        "y_max": y_max * spatial_resolution_xy,
        "width_min_bb": width_min_bb * spatial_resolution_xy,
        "length_min_bb": length_min_bb * spatial_resolution_xy,
        "geodeticlength": geodeticlength * spatial_resolution_xy,
        "thickness": thickness * spatial_resolution_xy,
        "n_erosions": n_erosions,
        "n_erosions_complement": n_erosions_complement,
        "fractal_dimension_boxcounting_method": fractal_dimension_boxcounting_method,
        "fractal_dimension_perimeter_method": fractal_dimension_perimeter_method,
        "feret_max": feret_max * spatial_resolution_xy,
        "feret_min": feret_min * spatial_resolution_xy,
        "feret_median": feret_median * spatial_resolution_xy,
        "feret_mean": feret_mean * spatial_resolution_xy,
        "feret_mode": feret_mode * spatial_resolution_xy,
        "feret_std": feret_std,
        "martin_max": martin_max * spatial_resolution_xy,
        "martin_min": martin_min * spatial_resolution_xy,
        "martin_median": martin_median * spatial_resolution_xy,
        "martin_mean": martin_mean * spatial_resolution_xy,
        "martin_mode": martin_mode * spatial_resolution_xy,
        "martin_std": martin_std,
        "nassenstein_max": nassenstein_max * spatial_resolution_xy,
        "nassenstein_min": nassenstein_min * spatial_resolution_xy,
        "nassenstein_median": nassenstein_median * spatial_resolution_xy,
        "nassenstein_mean": nassenstein_mean * spatial_resolution_xy,
        "nassenstein_mode": nassenstein_mode * spatial_resolution_xy,
        "nassenstein_std": nassenstein_std,
        "maxchords_max": maxchords_max * spatial_resolution_xy,
        "maxchords_min": maxchords_min * spatial_resolution_xy,
        "maxchords_median": maxchords_median * spatial_resolution_xy,
        "maxchords_mean": maxchords_mean * spatial_resolution_xy,
        "maxchords_mode": maxchords_mode * spatial_resolution_xy,
        "maxchords_std": maxchords_std,
        "allchords_max": allchords_max * spatial_resolution_xy,
        "allchords_min": allchords_min * spatial_resolution_xy,
        "allchords_median": allchords_median * spatial_resolution_xy,
        "allchords_mean": allchords_mean * spatial_resolution_xy,
        "allchords_mode": allchords_mode * spatial_resolution_xy,
        "allchords_std": allchords_std
    }

    statistical_lengths = {
        "measured_angles": measured_angles,
        "feret_diameters": feret_diameters * spatial_resolution_xy,
        "martin_diameters": martin_diameters * spatial_resolution_xy,
        "nassenstein_diameters": nassenstein_diameters * spatial_resolution_xy,
        "maxchords": maxchords * spatial_resolution_xy
    }

    all_chords = allchords * spatial_resolution_xy

    return df_2d, statistical_lengths, all_chords
