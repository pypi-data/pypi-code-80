#!/usr/bin/env python3
# coding: utf-8
# @Author: ArthurBernard
# @Email: arthur.bernard.92@gmail.com
# @Date: 2020-08-28 19:39:31
# @Last modified by: ArthurBernard
# @Last modified time: 2020-08-28 19:39:53

""" Script to compute the best time period. """

# Built-in packages

# Third party packages
import numpy as np

# Local packages
import fynance as fy


def compute_proba(x, fees):
    """ Compute the threasold probability.

    Parameters
    ----------
    x : np.ndarray
        Series of returns.
    fees : float
        Fees applied at each transaction in percentage.

    Returns
    -------
    float
        The minimal probability to get profit.

    """
    r = np.mean(np.abs(x))
    p = (fees / r + 1) / 2

    return p


def compute_returns(proba, fees):
    """ Compute the threasold returns.

    Parameters
    ----------
    proba : float
        Series of returns.
    fees : float
        Fees applied at each transaction in percentage.

    Returns
    -------
    float
        The minimal returns to get profit. 

    """
    return fees / (2 * proba - 1)


def compute_mini_period(x, fees, proba):
    """ Compute the minimal periods.

    Parameters
    ----------
    x : np.ndarray
        Series of returns.
    fees : float
        Fees applied at each transaction in percentage.
    proba : float
        Series of returns.

    Returns
    -------
    int
        The minimal number of period to get profit. And returns None if no period match the profit requirement.

    """
    N = x.size()
    n = 1
    while n < N:
        for m in range(1, min(n, N - n) + 1):
            r = np.mean(np.abs(fy.ma(x, n)[m::n]))
            if r > compute_returns(proba, fees):

                return n

        n += 1

    return None


if __name__ == "__main__":
    pass
