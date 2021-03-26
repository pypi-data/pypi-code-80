"""Helping functions to draw shapes on images."""

import cv2
import numpy as np


def polyline_on_img(img, polyline, color=(1, 0, 0), thickness=1, closed_line=True):
    """Draw polyline on image.

    Parameters
    ----------
    img : numpy.ndarray, type float
        RGB image in range [0, 1].
    polyline : np.ndarray, type int
        Array with points of polyline of shape
        [[x0, y0], [x1, y1], [x2, y2], ...].
    color : tuple, type float, optional
        RGB colors of drawing in range [0,1],
        color format: (R, G, B), by default (1, 0, 0).
    thickness : int, optional
        Thickness of drawing in pixel, by default 1.
    closed_line : bool, optional
        If true line will be closed (start and end point connected),
        by default True.

    Returns
    -------
    float
        - `img_with_line` (numpy.ndarray, type float):
            RGB image with drawn line in range [0, 1].
    """
    # convert color into 8bit opencv friendly format:
    color_8bit = (int(255 * color[0]),
                  int(255 * color[1]),
                  int(255 * color[2]))
    thickness = int(thickness)

    # transform image to 8bit (neccassary for cv2 drawing function)
    img_8bit = (img * 255).astype('uint8')

    # transform points into cv2 coordinate system
    polyline_cv2 = np.zeros(polyline.shape)
    polyline_cv2[:, 0], polyline_cv2[:, 1] = polyline[:, 1], polyline[:, 0]
    # transform points into cv2 friendly format
    polyline_trans = polyline_cv2.reshape((-1, 1, 2))
    # transform to integers for drawing
    polyline_trans = [polyline_trans.astype('int')]

    # draw line on images
    img_with_line = cv2.polylines(img_8bit,
                                  polyline_trans,
                                  closed_line,
                                  color_8bit,
                                  thickness=thickness)

    # back to [0,1]
    img_with_line = img_with_line / 255
    return img_with_line


def circle_on_img(img, center, diameter, color=(1, 0, 0), thickness=1, mark_centroid=True):
    """Draw circle on an image.

    Parameters
    ----------
    img : numpy.ndarray, type float
        RGB image in range [0, 1].
    center : numpy.ndarray, type int
        Center of circle in shape [x, y].
    diameter : int
        Diameter of circle.
    color : tuple, type float, optional
        RGB colors of drawing in range [0,1],
        color format: (R, G, B), by default (1, 0, 0).
    thickness : int, optional
        Thickness of drawing in pixel, by default 1.
    mark_centroid : bool, optional
        If True, centroid will be marked, by default True.

    Returns
    -------
    float
        - `img_with_circle` (numpy.ndarray, type float):
            RGB image with drawn circle in range [0,1].
    """
    # transform center into opencv-friendly format
    # (change coordinate system, change to integer, use tuple)
    center_coordinates = (int(center[1]), int(center[0]))

    # transform to radius and dtype int
    radius = int(diameter / 2)
    thickness = int(thickness)

    # convert color into 8bit opencv friendly format:
    color_8bit = (int(255 * color[0]),
                  int(255 * color[1]),
                  int(255 * color[2]))

    # transform image to 8bit (neccassary for cv2 drawing function)
    img_8bit = (img * 255).astype('uint8')

    # draw line on images
    img_with_circle = cv2.circle(img_8bit,
                                 center_coordinates,
                                 radius,
                                 color_8bit,
                                 thickness=thickness)

    # back to [0,1]
    img_with_circle = img_with_circle / 255

    if mark_centroid:
        img_with_circle = marker_on_img(img_with_circle,
                                        center,
                                        color=color,
                                        marker_size=20,
                                        marker_thickness=thickness)

    return img_with_circle


def marker_on_img(img, marker_pos, color=(1, 0, 0), marker_size=20, marker_thickness=3):
    """Draw marker on image.

    Parameters
    ----------
    img : numpy.ndarray, type float
        RGB image in range [0, 1].
    marker_pos : numpy.ndarray, type int
        Marker position in shape [x, y].
    color : tuple, type float, optional
        RGB colors of drawing in range [0,1],
        color format: (R, G, B), by default (1, 0, 0).
    marker_size : int, optional
        Size of  marker in pixel, by default 20
    marker_thickness : int, optional
        Thickness of drawing in pixel, by default 3.

    Returns
    -------
    float
        - `img_with_marker` (numpy.ndarray, type float):
            RGB image with drawn circle in range [0,1].
    """
    dl = int(marker_size / 2)
    dx = np.array([dl, 0])
    dy = np.array([0, dl])

    vertical_line = np.array([marker_pos + dx, marker_pos - dx])
    img_with_marker = polyline_on_img(img,
                                      vertical_line,
                                      color=color,
                                      thickness=marker_thickness)

    horizontal_line = np.array([marker_pos + dy, marker_pos - dy])
    img_with_marker = polyline_on_img(img_with_marker,
                                      horizontal_line,
                                      color=color,
                                      thickness=marker_thickness)

    return img_with_marker
