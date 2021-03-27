#!/usr/bin/env python3
# coding: utf-8
# @Author: ArthurBernard
# @Email: arthur.bernard.92@gmail.com
# @Date: 2019-03-28 18:12:52
# @Last modified by: ArthurBernard
# @Last modified time: 2019-11-18 09:12:20

""" Some filter functions. """

# Built-in packages

# External packages
import numpy as np

# Local packages


__all__ = []

# TODO : to finish kalman filter


def kalman(X, distribution='normal'):
    r""" Compute the Kalman filter.

    /! not yet working /!

    Kalman filter is computed as described in the paper by G. Welch and
    G. Bishop [1]_.

    Notes
    -----
    Let a vector :math:`x_t = \begin{bmatrix} p_t \\ v_t \end{bmatrix}` where
    :math:`p_t` is the position (or price) and :math:`v_t` is the velocity (or
    return) at time :math:`t`.

    We use basic kinematic formula:

    .. math:

        p_t = p_{t-1} + \Delta t v_{t-1} \\
        v_t = v_{t-1}

    Let :math:`F_t` the transformation matrix and :math:`\Omega_t` the
    covariance matrix of variables :math:`p_t` and :math:`v_t` at time
    :math:`t`:

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



    Parameters
    ----------
    X : array_like
        Observed data.
    distribution : str, optional
        An available distribution in scipy library.

    Returns
    -------
    array_like
        Filter of kalman following the given distribution.

    References
    ----------
    .. [1] https://www.cs.unc.edu/~welch/media/pdf/kalman_intro.pdf

    """
    T, n = X.shape

    # Initial estimation
    # TODO : Check better initialization
    m_0 = 0
    C_0 = 1

    # Set variables
    # TODO : Check shape of variables
    # ``a`` is the predicted states vector
    a = np.zeros([T, n])
    # ``R`` is the predicted 
    R = np.zeros([T, n])

    # F = ?
    # G = ?

    for t in range(1, T):
        # Time update (predict)
        a[t] = G[t] @ m[t - 1]
        R[t] = G[t] @ C[t - 1] @ G[t].T + W[t]

        # Measurement update (correct)
        A[t] = R[t] @ F[t] @ np.linalg.pinv(F[t] @ R[t] @ F[t].T + V[t])
        m[t] = a[t] + A[t] @ (X[t] - F[t].T @ a[t])
        C[t] = (np.identity(n) - A[t] @ F[t]) @ R[t]

    s_0 = 0
    x_0 = X[0]

    x_hat_1

####


def kf(Z, dim_state, A=None, B=None, U=None):
    r""" Kalman filter.

    Notes
    -----
    Discrete Kalman filter algorthm

    .. math::

        \hat{x}^-_t = A_t \hat{x}_{t-1} + B_t u_t

    Parameters
    ----------
    Z : np.ndarray[dtype, ndim=1 or 2]
        Observed data (measurement, etc.).
    dim_state : int or tuple of int
        Dimension of state.


    """
    shape = X.shape
    T = shape[0]

    for t in range(1, T):
        # prediction at time t
        # a priori expected state estimate
        X_m[t] = A @ X[t - 1] + B @ U[t]
        # a posteriori covariance state estimate
        P_m[t] = A @ P[t - 1] @ A.T + Q

        # Update at time t
        # kalman gain
        K[t] = P_m[t] @ H.T @ np.linalg.pinv(H @ P_m[t] @ H.T + R)
        # a posteriori expected state estimate
        X[t] = X_m[t] + K[t] @ (Z[t] - H @ X_m[t])
        # a posteriori covariance state estimate
        P[t] = (np.identity(n) - K[t] @ H) @ P_m[t]



        y[t] = H @ x[t] + v[t]


