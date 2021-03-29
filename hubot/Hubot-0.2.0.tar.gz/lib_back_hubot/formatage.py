from typing import List
import numpy as np
import pandas as pd


def format_metric(kpi_result, kpi_info: dict):
    """Format in a json serialisable way the result of a kpi metric

    Parameters
    ----------
    kpi_result: int or float or np.integer or np.floating
        the result of a metric kpi
    kpi_info: dict
        additional information about the kpi

    Returns
    -------
    int or float
        the kpi value
    """

    result = 0
    if isinstance(kpi_result, (np.integer, int)):
        result = int(kpi_result)
    elif isinstance(kpi_result, (np.floating, float)):
        result = float(kpi_result)
    else:
        excption_str = "Wrong data type for a metric : "+type(kpi_result)
        excption_str += "should be int, float, np.integer or np.floating"
        raise Exception(excption_str)

    return result


def format_pie(kpi_result: pd.DataFrame, kpi_info: dict) -> dict:
    """Format in a json serialisable way the result of a pie metric

    Parameters
    ----------
    kpi_result: pd.DataFrame
        the result of a pie KPI
    kpi_info: dict
        additional information about the kpi

    Returns
    -------
    dict
        the kpi values
    """
    label = []
    value = []
    tmp_dic = kpi_result.to_dict('index')
    for k in tmp_dic:
        label.append(k)
        value.append(tmp_dic[k][kpi_info['value']])

    return {
        'label': label,
        'value': value
    }


def format_timeline(kpi_result: pd.DataFrame, kpi_info: dict) -> List[dict]:
    """Format in a json serialisable way the result of a timeline metric

    Parameters
    ----------
    kpi_result: pd.DataFrame
        the result of a timeline KPI
    kpi_info: dict
        additional information about the kpi

    Returns
    -------
    List[dict]
        the kpi values (a list of dict, with one dict for each line)
    """

    result = []
    kpi_result = kpi_result.reset_index()

    if "group_col" in kpi_info:
        group_col = kpi_info["group_col"]
        for val in kpi_result[group_col].unique():
            tmp_data = kpi_result[kpi_result[group_col] == val]
            tmp_res = {}
            tmp_res['x'] = tmp_data[kpi_info['x']].values.tolist()
            tmp_res['y'] = tmp_data[kpi_info['y']].values.tolist()
            tmp_res['label'] = val
            result.append(tmp_res)

    else:
        tmp_res = {}
        tmp_res['x'] = kpi_result[kpi_info['x']].values.tolist()
        tmp_res['y'] = kpi_result[kpi_info['y']].values.tolist()
        result.append(tmp_res)
    return result


def apply_format(kpi_result: dict, kpi_info: dict, kpi_type: str) -> dict:
    """Apply the correct format function to a kpi result depending of its type

    Parameters
    ----------
    kpi_result: pd.DataFrame
        the result of a KPI
    kpi_info: dict
        additional information about the kpi
    kpi_type: str
        the type of the kpi

    Returns
    -------
    dict
        the formated KPI and its informations
    """

    func_result = dico_format_function[kpi_type]
    func_variation = dico_format_variation_function[kpi_type]

    result = {
        'type': kpi_type,
        'info': kpi_info,
        'result': func_result(kpi_result["result"], kpi_info)
    }

    if 'comparison' in kpi_result:
        result['variation'] = func_variation(kpi_result['comparison'], kpi_info)

    return result


# Dictionnary containing for each KPI type the function to use to format the result
dico_format_function = {
    "metric": format_metric,
    "timeline": format_timeline,
    "pie": format_pie,
    "other": lambda x, _: x
}


# Dictionnary containing for each KPI type the function to use to format the variation of the kpi
dico_format_variation_function = {
    "metric": format_metric,
    "timeline": format_timeline,
    "pie": format_pie,
    "other": lambda x, _: x
}
