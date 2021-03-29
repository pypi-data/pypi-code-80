import pytest
from test.helper import load_file
import pandas as pd

from lib_back_hubot import get_variation_two_metrics, add_variation_column, \
                            add_difference_value_column


@pytest.mark.parametrize("directory, filename", [
    ("get_variation_two_metrics", "nominal"),
    ("get_variation_two_metrics", "null_denominator")
])
def test_get_variation_two_metrics(directory, filename):
    payload = load_file('payloads', 'function_calcul_variation', directory, filename)
    expectation = load_file('expectation', 'function_calcul_variation', directory, filename)

    result = get_variation_two_metrics(**payload)

    assert result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("add_variation_column", "nominal")
])
def test_get_variation_column(directory, filename):
    payload = load_file('payloads', 'function_calcul_variation', directory, filename)
    expectation = load_file('expectation', 'function_calcul_variation', directory, filename)

    df1 = pd.DataFrame(payload["df1"])
    result = add_variation_column(df1, payload["to_compare_col_name"])["result"]

    expectation = pd.DataFrame(expectation)

    pd.testing.assert_frame_equal(result, expectation)


@pytest.mark.parametrize("directory, filename", [
    ("add_variation_column", "missing_to_compare_col_name")
])
def test_add_variation_column_wrong_column(directory, filename):
    payload = load_file('payloads', 'function_calcul_variation', directory, filename)
    expectation = load_file('expectation', 'function_calcul_variation', directory, filename)

    df1 = pd.DataFrame(payload["df1"])
    result = add_variation_column(df1, payload["to_compare_col_name"])

    assert result == expectation


@pytest.mark.parametrize("directory, filename", [
    ("add_difference_value_column", "nominal"),
])
def test_add_difference_value_column(directory, filename):
    payload = load_file('payloads', 'function_calcul_variation', directory, filename)
    expectation = load_file('expectation', 'function_calcul_variation', directory, filename)

    df1 = pd.DataFrame(payload["df1"])
    result = add_difference_value_column(df1, payload["compared_col_name"])["result"]

    expectation = pd.DataFrame(expectation)

    pd.testing.assert_frame_equal(result, expectation)


@pytest.mark.parametrize("directory, filename", [
    ("add_difference_value_column", "missing_to_compare_col_name")
])
def test_get_variation_distribution_pie_wrong_column(directory, filename):
    payload = load_file('payloads', 'function_calcul_variation', directory, filename)
    expectation = load_file('expectation', 'function_calcul_variation', directory, filename)

    df1 = pd.DataFrame(payload["df1"])
    result = add_variation_column(df1, payload["compared_col_name"])

    assert result == expectation
