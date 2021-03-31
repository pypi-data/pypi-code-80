"""Helping functions to project 3D points on a 2D plane."""

def xyz_to_xy(p_3d):
    """Project 3D points to xy plane.

    Parameters
    ----------
    p_3d : numpy.ndarray
        3D pointcloud in shape `(n,3)`, where `n` is the number of points.

    Returns
    -------
    numpy.ndarray
        - `p_2d` (numpy.ndarray):
            Projected pointcloud in shape `(n, 2)`,
            where `n` is the number of points.
    """
    p_2d = p_3d[:, [0, 1]]
    return p_2d


def xyz_to_xz(p_3d):
    """Project 3D points to xy plane.

    Parameters
    ----------
    p_3d : numpy.ndarray
        3D pointcloud in shape `(n,3)`, where `n` is the number of points.

    Returns
    -------
    numpy.ndarray
        - `p_2d` (numpy.ndarray):
            Projected pointcloud in shape `(n,2)`,
            where `n` is the number of points.
    """
    p_2d = p_3d[:, [0, 2]]
    return p_2d


def xyz_to_yz(p_3d):
    """Project 3D points to xy plane.

    Parameters
    ----------
    p_3d : numpy.ndarray
        3D pointcloud in shape `(n,3)`,
        where `n` is the number of points.

    Returns
    -------
    numpy.ndarray
        - `p_2d` (numpy.ndarray):
            Projected pointcloud in shape `(n, 2)`,
            where `n` is the number of points.
    """
    p_2d = p_3d[:, [1, 2]]
    return p_2d
