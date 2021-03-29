from typing import Union
import pandas as pd
import numpy as np


def get_variation_two_metrics(res1: Union[int, float], res2: Union[int, float]) -> dict:
    """Get the variation rate between two metrics

    Parameters
    ----------
    res1 : Union[int, float]
        initial value
    res2 : Union[int, float]
        end value

    Returns
    -------
    float
        result of variation rate
    """
    if res1 != 0:
        return {"result": (res2 - res1) / res1}

    return {"result": ""}


def add_variation_column(to_compare_data: pd.DataFrame, to_compare_col_name: str) -> dict:
    """Compute variation rate between the values of two columns beggining with `to_compare_col_name`

    Parameters
    ----------
    to_compare_data : pd.DataFrame
        Data containing the two columns between which we will calculate the variation rate
    to_compare_col_name : str
        Name of the column whose evolution is computed

    Returns
    -------
    dict
        As a result the initial DataFrame enriched with one column containing
        the variation rate of each row
    """

    if (to_compare_col_name + "_x" not in to_compare_data.columns or
            to_compare_col_name + "_y" not in to_compare_data.columns):
        return {"error": f"One of the column {to_compare_col_name} is missing in dataframe"}

    start = to_compare_data[to_compare_col_name + "_x"].to_numpy()
    end = to_compare_data[to_compare_col_name + "_y"].to_numpy()

    comparison_result = to_compare_data.copy()

    variation_col_name = "evolution_" + to_compare_col_name
    comparison_result[variation_col_name] = (end - start) / start

    comparison_result = comparison_result.replace([np.inf, -np.inf], np.nan)

    return {"result": comparison_result}


def add_difference_value_column(to_compare_data: pd.DataFrame, to_compare_col_name: str) -> dict:
    """Compute the difference between the values of the two columns beggining with `to_compare_col_name`

    Parameters
    ----------
    to_compare_data : pd.DataFrame
        Data containing the two columns between which we will calculate the variation rate
    to_compare_col_name : str
        Name of the column whose evolution is computed

    Returns
    -------
    dict
        As a result the initial DataFrame enriched with one column containing
        the value difference of each row
    """

    if (to_compare_col_name + "_x" not in to_compare_data.columns or
            to_compare_col_name + "_y" not in to_compare_data.columns):
        return {"error": f"One of the column {to_compare_col_name} is missing in dataframe"}

    comparison_result = to_compare_data.copy()

    # Don't compare row with NaN value in one of the column
    comparison_result = comparison_result.dropna()

    previous = comparison_result[to_compare_col_name + "_x"]
    current = comparison_result[to_compare_col_name + "_y"]

    comparison_result["evolution_" + to_compare_col_name] = current - previous

    return {"result": comparison_result}
