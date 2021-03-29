# (c) 2014-2021 Dr. Flavio ABREU ARAUJO

import numpy as np
from scipy.signal import hilbert
from math import ceil

# Simple Numerical Instantaneous Frequency Approximation (SNIFA)
#
# [IN] T = time array where each element corresponds to an element in
#          the signal arrays X and Y.
# [IN] X = array containing the x components of the oscillating signal
# [IN] Y = (optional) array containing the y components of the oscillating signal
#
# [OUT]    t = resulting time array
# [OUT]    f = resulting frequency array
# [OUT] filt = scalar giving the mean number of elements for 1 cycle
def SNIFA(T, X, Y=[]):
    if Y == []:
        Y = -np.imag(hilbert(X))
    signal = X + 1j * Y
    inst_phase = np.unwrap(np.angle(signal))
    dT, dphi = np.diff(T), np.diff(inst_phase)
    assert not any(dT <= 0), 'T is NOT monotonically increasing!'
    f = dphi / (2.0*np.pi * dT)
    filt = np.floor(2.0*np.pi/np.abs(np.mean(dphi)))+1
    t = T[1::]
    return t, f, filt


# Angles between 2D vectors in an array of vectors
# Alternative to numpy angle() not using complex numbers
def ANG(V):
    V1 = V[:,:-1]; V2 = V[:,1::]
    SP = np.sum(V1*V2, axis=0) # Scalar product
    Nv = np.sqrt(np.sum(V*V, axis=0)) # Norm of vectors inside V
    ang = np.arccos(SP/(Nv[:-1]*Nv[1::]))
    return ang


#* Alternative to SNIFA()
def SNIFA_ALT(T, X, Y=[]):
    if Y == []:
        Y = np.imag(hilbert(X))
    dT = np.diff(T)
    assert not any(dT <= 0), 'T is NOT monotonically increasing!'
    t = T[1::]
    V = np.vstack((X, Y))
    alpha = np.real(ANG(V))
    f = alpha/(2.0*np.pi*dT)
    filt = np.floor(2.0*np.pi/np.mean(alpha))+1
    return t, f, filt


#* Compute the moving average
def mv_avg(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


#* Compute de filtered SNIFA
def filt_freq(T, X, Y=[], w_filt=1):
    assert (len(T) == len(X)) & (len(T) > 1), 'Data is not consistant.'
    t, f, filt = SNIFA(T, X, Y)
    if w_filt == 0:
        return t, f
    else:
        w = ceil(w_filt*filt)
        assert w > 0, 'Moving avg window must be >0.'
        assert len(T) > w+1, 'Window is too wide for the amount of data.'
        f_filt = mv_avg(f, w)
        return t[w-1::], f_filt
