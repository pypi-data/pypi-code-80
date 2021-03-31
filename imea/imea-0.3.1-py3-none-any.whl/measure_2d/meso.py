"""2-dimensional mesodescriptors."""

import warnings
from skimage import morphology
import numpy as np


def erosions_till_erase_complement(bw, bw_convex, pad_width=1, selem=None, return_counts=False):
    """Determine number of erosions that are necessary to erase all pixels
    from the complement between the binary image of
    an object and the binary image of its convex hull [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    bw_convex : numpy.ndarray, type bool
        2-dimensional binary image of convex hull corresponding to `bw`.
    pad_width : int, optional
        Number of false pixels to pad around the image, by default 1.
    selem : numpy.ndarray, type bool, optional
        Neighborhood expressed as a 2-D array of ones and zeros, by default None.
        If None, use a cross-shaped structuring element (connectivity=1) is used.
    return_counts : bool, optional
        If True, a list with the number of true pixels for each iteration is returned,
        by default False.

    Returns
    -------
    tuple
        - `n_erosions_2d` (int):
            Number of erosions to fully erase complement between `bw` and `bw_convex`.
        - `true_pixels_per_erosion` (numpy.ndarray, optional):
            Number of true pixels after each erosion. Only provided if
            `return_counts` is True.

    References
    ----------
    [1] Deutsches Institut für Normung e. V. (2012). DIN ISO 9276-6 -
        Darstellung der Ergebnisse von Par-tikelgrößenanalysen:
        Teil 6: Deskriptive und quantitative Darstellung der Form
        und Morphologie von Partikeln.
    """
    assert bw.ndim == 2, "Binary image must be 2-dimensional."
    assert bw.shape == bw_convex.shape, ' '.join(("Binary image and complement should have",
                                                  "same shape, but have shape bw:",
                                                  " {} and shape bw_complement: {}".format(
                                                      bw.shape,
                                                      bw_convex.shape)
                                                  ))

    bw_non_object = np.logical_not(bw)
    bw_complement = np.logical_and(bw_convex, bw_non_object)

    return erosions_till_erase(bw_complement,
                               pad_width=pad_width,
                               selem=selem,
                               return_counts=return_counts)


def erosions_till_erase(bw, pad_width=1, selem=None, return_counts=False):
    """Determine number of erosions that are necessary to fully erase
    all True elements in a binary image [1].

    Parameters
    ----------
    bw : numpy.ndarray, type bool
        2-dimensional binary image.
    pad_width : int, optional
        Number of false pixels to pad around the image, by default 1.
    selem : numpy.ndarray, type bool, optional
        Neighborhood expressed as a 2-D array of ones and zeros, by default None.
        If None, use a cross-shaped structuring element (connectivity=1) is used.
    return_counts : bool, optional
        If True, a list with the number of true pixels for each iteration
        is returned, by default False.

    Returns
    -------
    tuple
        - `n_erosions_2d` (int):
            Number of erosions to fully erase true pixels from image.
        - `true_pixels_per_erosion` (numpy.ndarray, optional):
            Number of true pixels after each erosion. Only provided if
            `return_counts` is True.

    References
    ----------
    [1] Deutsches Institut für Normung e. V. (2012). DIN ISO 9276-6 -
        Darstellung der Ergebnisse von Par-tikelgrößenanalysen:
        Teil 6: Deskriptive und quantitative Darstellung der Form
        und Morphologie von Partikeln.
    """
    assert bw.ndim == 2, "Binary image must be 2-dimensional."

    if np.count_nonzero(bw) == 0:
        if return_counts:
            return 0, np.array([])
        else:
            return 0

    bw_eroded = np.pad(bw,
                       pad_width=pad_width,
                       mode='constant',
                       constant_values=False)

    true_pixels_per_erosion = []
    true_pixels_per_erosion.append(np.count_nonzero(bw_eroded))

    while true_pixels_per_erosion[-1] > 0:
        bw_eroded = morphology.binary_erosion(bw_eroded)
        true_pixels_per_erosion.append(np.count_nonzero(bw_eroded))

    n_erosions_2d = len(true_pixels_per_erosion)

    if return_counts:
        return n_erosions_2d, np.array(true_pixels_per_erosion)
    else:
        return n_erosions_2d
