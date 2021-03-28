import numpy as np

def chain(a: np.ndarray, b: np.ndarray, *args) -> np.ndarray:
    if len(args) > 0:
        b = chain(b, *args)
    return np.dot(b, a)
