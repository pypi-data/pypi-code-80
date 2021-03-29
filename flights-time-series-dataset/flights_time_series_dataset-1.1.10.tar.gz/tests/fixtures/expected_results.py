import os
from pathlib import Path

import numpy as np
import pytest

filepath = Path(os.path.split(__file__)[0])

expected = {}
with \
    open(Path.joinpath(filepath, 'size_stride_1_test_x.npy'), 'rb') as f_1_test_x, \
    open(Path.joinpath(filepath, 'size_stride_1_test_y.npy'), 'rb') as f_1_test_y, \
    open(Path.joinpath(filepath, 'size_stride_1_x.npy'), 'rb') as f_1_x, \
    open(Path.joinpath(filepath, 'size_stride_1_y.npy'), 'rb') as f_1_y:
    x = np.load(f_1_x, allow_pickle = True)
    y = np.load(f_1_y, allow_pickle = True)
    test_x = np.load(f_1_test_x, allow_pickle = True)
    test_y = np.load(f_1_test_y, allow_pickle = True)
    expected = {
        "0": {
            'x': x,
            'y': y,
            'test_x': test_x,
            'test_y': test_y,
            "y_shape": (73, 24, 1),
            "x_shape": (73, 24, 2),
            "y_test_shape": (1, 24, 1),
            "x_test_shape": (1, 24, 2),
        },
        "1": {
            'x': x,
            'y': y,
            'test_x': test_x,
            'test_y': test_y,
            "y_shape": (73, 24, 1),
            "x_shape": (73, 24, 2),
            "y_test_shape": (1, 24, 1),
            "x_test_shape": (1, 24, 2),
        }
    }

@pytest.fixture
def expected_results():
    def _expected_results(augmentation):
        return expected[str(augmentation)]
    
    return _expected_results
