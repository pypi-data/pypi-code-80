import numpy as np
import scipy.spatial

__all__ = []


def deproject_points(x, y, z, fx, fy, cx, cy):
    """

    :param x: numpy.array y values of length N
    :param y: numpy.array y values of length N
    :param z: numpy.array z values of length N
    :param fx: Focal length x
    :param fy: Focal length y
    :param cx: Camera principal point x
    :param cy: Camera principal point y
    :return:
    """

    return x, y, z


def deproject_image(self, depth_image):
    """Deprojects a DepthImage into a PointCloud.
    Parameters
    ----------
    depth_image : :obj:`DepthImage`
        The 2D depth image to projet into a point cloud.
    Returns
    -------
    :obj:`autolab_core.PointCloud`
        A 3D point cloud created from the depth image.
    Raises
    ------
    ValueError
        If depth_image is not a valid DepthImage in the same reference frame
        as the camera.
    """
    # check valid input
    if not isinstance(depth_image, DepthImage):
        raise ValueError('Must provide DepthImage object for projection')
    if depth_image.frame != self._frame:
        raise ValueError('Cannot deproject points in frame %s from camera with frame %s' %(depth_image.frame, self._frame))

    # create homogeneous pixels
    row_indices = np.arange(depth_image.height)
    col_indices = np.arange(depth_image.width)
    pixel_grid = np.meshgrid(col_indices, row_indices)
    pixels = np.c_[pixel_grid[0].flatten(), pixel_grid[1].flatten()].T
    pixels_homog = np.r_[pixels, np.ones([1, pixels.shape[1]])]
    depth_arr = np.tile(depth_image.data.flatten(), [3,1])

    # deproject
    points_3d = depth_arr * np.linalg.inv(self._K).dot(pixels_homog)
    # return PointCloud(data=points_3d, frame=self._frame)

def deproject(self, depth_image):
    """Deprojects a DepthImage into a PointCloud.
    Parameters
    ----------
    depth_image : :obj:`DepthImage`
        The 2D depth image to projet into a point cloud.
    Returns
    -------
    :obj:`autolab_core.PointCloud`
        A 3D point cloud created from the depth image.
    Raises
    ------
    ValueError
        If depth_image is not a valid DepthImage in the same reference frame
        as the camera.
    """
    # check valid input
    if not isinstance(depth_image, DepthImage):
        raise ValueError('Must provide DepthImage object for projection')
    if depth_image.frame != self._frame:
        raise ValueError('Cannot deproject points in frame %s from camera with frame %s' %(depth_image.frame, self._frame))

    # create homogeneous pixels
    row_indices = np.arange(depth_image.height)
    col_indices = np.arange(depth_image.width)
    pixel_grid = np.meshgrid(col_indices, row_indices)
    pixels = np.c_[pixel_grid[0].flatten(), pixel_grid[1].flatten()].T
    pixels_homog = np.r_[pixels, np.ones([1, pixels.shape[1]])]
    depth_arr = np.tile(depth_image.data.flatten(), [3,1])

    # deproject
    points_3d = depth_arr * np.linalg.inv(self._K).dot(pixels_homog)
    # return PointCloud(data=points_3d, frame=self._frame)