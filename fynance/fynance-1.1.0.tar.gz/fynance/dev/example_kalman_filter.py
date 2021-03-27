#!/usr/bin/env python3
# coding: utf-8
# @Author: ArthurBernard
# @Email: arthur.bernard.92@gmail.com
# @Date: 2019-11-13 14:58:00
# @Last modified by: ArthurBernard
# @Last modified time: 2019-11-18 09:12:35

r""" Example of computing kalman filter.

Let a vector :math:`x_t = \begin{bmatrix} p_t \\ v_t \end{bmatrix}` where
:math:`p_t` is the position (or price) and :math:`v_t` is the velocity (or
return) at time :math:`t`.

We use basic kinematic formula:

.. math:

    p_t = p_{t-1} + \Delta t v_{t-1} \\
    v_t = v_{t-1}

Let :math:`F_t` the transformation matrix and :math:`\Omega_t` the covariance
matrix of variables :math:`p_t` and :math:`v_t` at time :math:`t`:

.. math:

    x_t = \begin{bmatrix}
    1 & \Delta t \\
    0 & 1
    \end{bmatrix} x_{t-1} \\
    x_t = F_t x_{t-1} \\
    \Omega_t = F_t \Omega_{t-1} F_t^T

Let :math:`u_t` are external influences and :math:`Q_t` are external
uncertainties:

.. math::

    \hat{x}_t = F_t \hat{x}_{t-1} + B_t u_t \\
    \Omega_t = F_t \Omega_{t-1} F_t + Q_t

"""

# Built-in packages

# Third party packages
import numpy as np

# Local packages
import fynance as fy


def kalman_filter(X):
    """ Compute the Kalman filter. """
    