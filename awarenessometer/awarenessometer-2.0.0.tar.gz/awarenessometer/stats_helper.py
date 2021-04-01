import math
import itertools
from typing import Union, List

import mpmath
import scipy.integrate as integrate
import numpy as np
from scipy.stats import pearsonr


def _ignorance(x: int,  # pylint: disable=invalid-name
               p_nopos_neg: float,
               p_nopos: float) -> Union[mpmath.mpf, int]:
    ign = mpmath.fmul(p_nopos_neg, mpmath.power(p_nopos, x - 1))
    if math.isnan(ign):
        return 1
    if ign > 1:
        return 1
    return ign


def collective_awareness(p_nopos_neg: float,
                         p_nopos: float,
                         employees_with_vdu: int) -> mpmath.mpf:
    area = integrate.quad(lambda x: _ignorance(x, p_nopos_neg, p_nopos), 1, employees_with_vdu)[0]
    total_area = mpmath.fdiv(1, employees_with_vdu - 1)
    share_area = mpmath.fmul(area, total_area)
    return mpmath.fsub(1, share_area)


def artifact_correlations(matrix: np.array) -> List[float]:
    mean = np.nanmean(matrix)

    def de_nan(val: float) -> float:
        return mean if np.isnan(val) else val

    correlations = []
    no_artifacts = matrix.shape[1]
    for artifact_index1, artifact_index2 in itertools.combinations(np.arange(no_artifacts), 2):
        artifact_1_values = matrix[:, artifact_index1]
        artifact_2_values = matrix[:, artifact_index2]

        values1: List[float] = [de_nan(val) for val in artifact_1_values]
        values2: List[float] = [de_nan(val) for val in artifact_2_values]
        correlations.append(pearsonr(values1, values2)[0])
    return correlations


def cronbachs_alpha(correlations: List) -> float:
    no_correlations = len(correlations)
    mean_correlation = sum(correlations) / no_correlations
    return (no_correlations * mean_correlation) / (1 + (no_correlations - 1) * mean_correlation)
