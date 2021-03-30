# Module: RecFeatureSelect
# Author: Daniel Ryan Furman <dryanfurman@gmail.com>
# License: MIT
# Last modified : 3.10.2021

import numpy as np
import pandas as pd
import os

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
test_data = [
    os.path.join(DATA, x)
    for x in ['feature-correlations-test.csv','feature-importance-test.csv',
        'raw-data-test.csv']]

# Unit tests for the feature selection algorithm.
covariance_org = pd.read_csv(test_data[0])
feature_importance = pd.read_csv(test_data[0])
threshold = 0.85
raw_data = pd.read_csv(test_data[0])

def test_inputs():
    # First assert that the inputs have the same features (and order)
    assert np.all(covariance_org.columns == feature_importance.columns)
    assert list(covariance_org) == list(feature_importance)

def test_function():
    # Second, assert that all final correlations are lower than the threshold
    from RecFeatureSelect import feature_selector
    feature_selector(covariance_org, feature_importance, threshold, raw_data)
    cov = pd.read_csv('data/cov.csv', index_col = "Unnamed: 0")
    cov = cov.to_numpy()
    np.fill_diagonal(cov, 0)
    # did the algorithm remove correlated pairs above the threshold? :
    assert np.all(cov <= threshold)
