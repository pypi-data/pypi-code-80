"""Helping functions to preprocess 3d heightmap images for shape measurement extraction."""

import warnings

import numpy as np
import pandas as pd
from skimage import measure


def extract_and_preprocess_3d_imgs(img_3d, threshold_gv, min_object_area=0, max_objects=-1):
    """Segment 3d image and return list of 3d images of single objects and corresponding binary images.

    Parameters
    ----------
    img_3d : numpy.ndarray, type float
        2-dimensional grayscale heightmap.
        Pixels not showing the pixel should be 0.
    threshold_gv : float
        Threshold in grayvalues for segmentation of `img_3d`.
    min_object_area : int, optional
        Minimum number of pixels for a region to be considered
        as an object, by default 0.
    max_objects : int, optional
        Maximum number of objects to be extracted,
        If `max_objects=-1`, then all objects are extracted,
        by default -1.

    Returns
    -------
    tuple
        - `imgs_3d` (list):
            List of cropped 3d images as numpy.ndarray for each object.
        - `bws` (list):
            List of cooresponding binary images.
    """
    # Segmentation
    bw = img_3d >= threshold_gv

    if np.count_nonzero(bw.ravel()) == 0:
        warnings.warn(
            "img_3d does not contain any objects. Check image and adjust threshold.")
        return [], []

    # Object extraction
    df = pd.DataFrame(measure.regionprops_table(measure.label(
        bw), intensity_image=img_3d, properties=('area', 'bbox', 'image', 'intensity_image')))

    # Remove small objects
    df = df[df['area'] > min_object_area]
    df = df.sort_values('area', ascending=False).reset_index(drop=True)

    n_objects_found = len(df)

    if max_objects <= 0:
        n_objects_to_extract = n_objects_found
    else:
        n_objects_to_extract = min(n_objects_found, max_objects)

    # Order extracted objects into list
    imgs_3d = []
    bws = []
    for i in range(n_objects_to_extract):
        bw_cropped = df['image'][i]
        img_3d_cropped = df['intensity_image'][i]
        img_3d_cropped[~bw_cropped] = 0
        bws.append(bw_cropped)
        imgs_3d.append(img_3d_cropped)

    return imgs_3d, bws


def equalspace_3d_img(img_3d, spatial_resolution_xy, spatial_resolution_z=1.0):
    """Create a equalspace image, i. e. dx = dy = dz.

    Parameters
    ----------
    img_3d : numpy.ndarray, type float
        2-dimensional grayscale heightmap.
        Pixels not showing the pixel should be 0.
    spatial_resolution_xy : float
        Spatial resolution of `img_3d` in x and y direction in [mm/pixel].
    spatial_resolution_z : float, optional
        Spatial resolution of `img_3d` in z-direction (height) in [mm/grayvalue],
        by default 1.

    Returns
    -------
    tuple
        - `img_3d_equalspace` (numpy.ndarray, type float):
            3d image with `dx = dy = dz`.
        - `spatial_resolution` (float):
            Spatial resolution of `img_3d_equalspace`.

    Notes
    -----
    `spatial_resolution` is set to `spatial_resolution_xy`,
    as only heights are transformed.
    """
    resize_factor_z = spatial_resolution_xy/spatial_resolution_z
    img_3d_equalspace = img_3d / resize_factor_z

    # Definition of spatial resolution (see Notes):
    spatial_resolution = spatial_resolution_xy

    return img_3d_equalspace, spatial_resolution
