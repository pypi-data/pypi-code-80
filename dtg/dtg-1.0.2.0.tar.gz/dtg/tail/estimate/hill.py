import numpy as np
import numba as nb

from dtg.tail.estimate.estimator import TailEstimator


class HillEstimator(TailEstimator):
    @staticmethod
    @nb.njit(fastmath=True)
    def estimate(x, k):
        return np.mean(np.log(x[-k:])) - np.log(x[-k-1])

    @staticmethod
    def check(ex):
        if np.sum(np.isnan(ex)) + np.sum(np.isinf(ex)) > 0:
            return False
        if ex <= 0:
            return False
        return True
