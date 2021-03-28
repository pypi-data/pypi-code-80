import numpy as np

def xor(a, b):
    return np.logical_xor(a, b, dtype='uint8').astype("uint8")

def add(a, b):
    a, b = check_type(a, b)
    a, b = strip_zeros(a), strip_zeros(b)
    N = len(a)
    D = len(b)
    if N == D:
        res = xor(a, b)
    elif N > D:
        res = np.concatenate((xor(a[:D], b), a[D:]))
    else:
        res = np.concatenate((xor(a, b[:N]), b[N:]))
    return strip_zeros(res)

def mul(a, b):
    fsize = len(a) + len(b) - 1
    fsize = 2**np.ceil(np.log2(fsize)).astype(int) #use nearest power of two much faster
    fslice = slice(0, fsize)
    ta = np.fft.fft(a, fsize)
    tb = np.fft.fft(b, fsize)
    res = np.fft.ifft(ta*tb)[fslice].copy()
    k = np.mod(np.rint(np.real(res)), 2).astype('uint8')
    return strip_zeros(k)

def div(dividend, divisor):
    N = len(dividend) - 1
    D = len(divisor) - 1
    if dividend[N] == 0 or divisor[D] == 0:
        dividend, divisor = strip_zeros(dividend), strip_zeros(divisor)
    if not divisor.any():  # if every element is zero
        raise ZeroDivisionError("polynomial division")
    elif D > N:
        q = np.array([])
        return q, dividend
    else:
        u = dividend.astype("uint8")
        v = divisor.astype("uint8")
        m = len(u) - 1
        n = len(v) - 1
        scale = v[n].astype("uint8")
        q = np.zeros((max(m - n + 1, 1),), u.dtype)
        r = u.astype(u.dtype)
        for k in range(0, m - n + 1):
            d = scale and r[m - k].astype("uint8")
            q[-1 - k] = d
            r[m - k - n:m - k + 1] = np.logical_xor(r[m - k - n:m - k + 1], np.logical_and(d, v))
        r = strip_zeros(r)
    return q, r

def inv(f, g):
    out = xgcd(f, g)[0]
    return out

def xgcd(b, a):
    x1 = np.array([1], dtype="uint8")
    y0 = np.array([1], dtype="uint8")
    x0 = np.array([], dtype="uint8")
    y1 = np.array([], dtype="uint8")
    while True:
        q, r = div(b, a)
        b = a
        if not r.any():
            break
        a = r
        if not (q.any() and x1.any()):  # if q is zero or x1 is zero
            x2 = x0
        elif not x0.any():  # if x0 is zero
            x2 = _mul(x1, q)
        else:
            mulres = _mul(x1, q)
            x2 = add(x0, mulres)
        if not (q.any() and y1.any()):
            y2 = y0
        elif not y0.any():
            y2 = _mul(y1, q)
        else:
            mulres = _mul(y1, q)
            y2 = add(y0, mulres)
        # update
        y0 = y1
        x0 = x1
        y1 = y2
        x1 = x2
    return y2, x2, b

# alt mul with convolution rather than fft:
def _mul(a, b):
    out = np.mod(np.convolve(a, b), 2).astype("uint8")
    return strip_zeros(out)

def strip_zeros(a):
    return np.trim_zeros(a, trim='b')

def check_type(a, b):
    if isinstance(a, np.ndarray):
        a = np.array(a, dtype="uint8")
    if isinstance(b, np.ndarray):
        b = np.array(b, dtype="uint8")
    if a.dtype != "uint8":
        a = a.astype("uint8")
    if b.dtype != "uint8":
        b = b.astype("uint8")
    return a, b

def padding(a, dim):
    return np.pad(a, (0, dim-len(a)), 'constant', constant_values=(0))

def to_same_dim(a, b):
    if len(a) > len(b):
       return a, padding(b, len(a))
    elif len(a) < len(b):
        return padding(a, len(b)), b
    else:
        return a, b

def zeros(dim):
    return np.zeros(dim, dtype='uint8')


def zerodegree_pol(dim):
    out = zeros(dim)
    out[0] = 1
    return out
