from typing import List, Callable
from lib_back_hubot import list_cube, check_cubes, complete_filter_cube, convert_filters, \
                            filter_list_of_cubes, need_date_before, get_date_before_filter, \
                            list_cube_containing_date_before

from lib_back_hubot import check_cube_kpi, filter_correct_kpi, get_variation_two_metrics


from lib_back_hubot import get_all_kpi

from lib_back_hubot import apply_format

DATE_FILTERS = 'dates'
BASE_FILTERS = 'base'

KPI_TYPE_TO_VARIATION_FUNCTION = {
    "metric": get_variation_two_metrics
}


def get_all_valid_kpi_and_cubes(list_kpi: list,
                                kpi_functions: dict,
                                cube_loader: Callable[[List[str]], dict]):
    """Load all the cubes needed to process the kpi of list_kpi
    and check if each kpi is calculable

    Parameters
    ----------
    list_kpi : list
        the list of kpi wanted
    kpi_functions : dict
        the definition of all the kpi function
    cube_loader : Callable[[List[str]], dict]
        a callback use to load the cubes

    Returns
    -------
    [valid_kpi, error_kpi, loaded_cubes, valid_cubes, metric_cube]
    valid_kpi : list : list of all calculable kpi
    error_kpi : dict: dict containing uncalculable kpi and the reason
    loaded_cubes : dict : dict containing each cube needed as a dataframe
    valid_cubes : list : list of cubes corectly loaded
    metric_cube : list : list of cubes use for metrics kpi
    kpi_cube_names : dict : for each kpi, the cubes needed
    """

    # Get all the valid KPI to compute
    valid_kpi, error_kpi = filter_correct_kpi(list_kpi, kpi_functions)

    # Get all needed cube and load them
    cube_names, metric_cube, kpi_cube_names = list_cube(valid_kpi, kpi_functions)
    loaded_cubes = cube_loader(cube_names)

    # Get only the KPI whose cubes have been loaded correctly
    valid_cubes, missing_cube, invalid_cube = check_cubes(cube_names, loaded_cubes)
    valid_kpi, missing_cube_kpi = check_cube_kpi(valid_kpi, valid_cubes, kpi_cube_names)

    all_error_kpi = {}
    for kpi in error_kpi:
        all_error_kpi[kpi] = error_kpi[kpi]

    for kpi in missing_cube_kpi:
        all_error_kpi[kpi] = missing_cube_kpi[kpi]

    return valid_kpi, all_error_kpi, loaded_cubes, valid_cubes, metric_cube, kpi_cube_names


def get_filtered_cubes(filters: dict,
                       list_cubes: list,
                       loaded_cubes: dict,
                       date_format: str,
                       filters_to_cube_colname: dict,
                       filters_to_cube_values: dict) -> dict:
    """Filter a list of cubes with the filter wanted

    Parameters
    ----------
    filters : dict
        the filters use to filter the cubes
    list_cubes : list
        list of cubes to filter
    loaded_cubes : dict
        all the loaded cubes
    date_format : str
        the date format
    filters_to_cube_colname : dict, optional
        used to transform a filter key to a cube column name, by default {}
    filters_to_cube_values : dict, optional
        used to transform a filter value to a cube column value, by default {}

    Returns
    -------
    dict
        the filtered cubes

    """
    data_filters = filters[BASE_FILTERS]
    filters_to_cube_colname, filters_to_cube_values = complete_filter_cube(
        data_filters, filters_to_cube_colname, filters_to_cube_values
    )
    data_filters = convert_filters(
        data_filters, filters_to_cube_colname, filters_to_cube_values
    )
    filtered_cubes = filter_list_of_cubes(
        list_cubes, loaded_cubes, filters[DATE_FILTERS], data_filters, date_format
    )
    return filtered_cubes


def get_kpi_for_previous_period(list_kpi: List[str],
                                kpi_functions: dict,
                                loaded_cubes: dict,
                                filters: dict,
                                front_filters: dict,
                                external_calcul_functions: dict,
                                date_format: str) -> dict:
    """calculate the KPIs for the previous period, based on the initial period defined in the filters

    Parameters
    ----------
    list_kpi : List[str]
        list of kpi to calculate
    kpi_functions : dict
        the definition of each kpi (how to process it)
    loaded_cubes : dict
        the cubes loaded
    filters : dict
        the filters use to filter the cubes
    front_filters : dict, optional
        a dict containing specific filters needed for some KPIs.
    external_calcul_functions : dict, optional
        specific calcul fonction to add to the default ones, by default None
    date_format : str
        the date format

    Returns
    -------
    dict
        the result of the KPI calculation for the previous period
        return an empty dict if previous period is not applicable
    """
    kpi_to_calc = [kpi for kpi in list_kpi if kpi_functions[kpi]['type'] in KPI_TYPE_TO_VARIATION_FUNCTION]
    cube_needed, _, kpi_cube_names = list_cube(kpi_to_calc, kpi_functions)

    if need_date_before(cube_needed, filters[DATE_FILTERS]):
        dates_before_filters = get_date_before_filter(filters[DATE_FILTERS], date_format)
        date_before_cube_list = list_cube_containing_date_before(
            cube_needed, loaded_cubes, dates_before_filters, date_format
        )
        date_before_cube = filter_list_of_cubes(
            date_before_cube_list, loaded_cubes, dates_before_filters, filters[BASE_FILTERS], date_format
        )

        kpi_to_calc, missing_cube_before_kpi = check_cube_kpi(
            kpi_to_calc, date_before_cube_list, kpi_cube_names
        )

        result = get_all_kpi(
            kpi_to_calc,
            kpi_functions,
            front_filters,
            date_before_cube,
            external_calcul_functions
        )

        return result
    else:
        return {}


def add_comparaison_to_result(result: dict, previous_result: dict, kpi_functions: dict) -> dict:
    """compare the result in result with those in previous_result

    Parameters
    ----------
    result : dict
        the base result
    previous_result : dict
        the result for the previous period
    kpi_functions : dict
        the definition of each kpi

    Returns
    -------
    dict
        result with comparaison information added
    """
    for kpi in previous_result:
        if "error" not in previous_result[kpi]:
            kpi_result = result[kpi]["result"]
            comparaison = previous_result[kpi]["result"]
            kpi_type = kpi_functions[kpi]['type']
            result[kpi]['comparaison'] = KPI_TYPE_TO_VARIATION_FUNCTION[kpi_type](kpi_result, comparaison)

        else:
            result[kpi]['comparaison'] = previous_result[kpi]['error']
    return result


def format_kpi_result(result_kpi: dict, kpi_functions: dict) -> dict:
    """format the result of the kpi

    Parameters
    ----------
    result_kpi : dict
        the result of the kpi
    kpi_functions : dict
        the kpi definition

    Returns
    -------
    dict
        the formated result
    """
    formated_result = {}
    for kpi in result_kpi:
        if "result" in result_kpi[kpi]:
            formated_result[kpi] = apply_format(result_kpi[kpi],
                                                kpi_functions[kpi]["info"],
                                                kpi_functions[kpi]["type"])
        else:
            formated_result[kpi] = result_kpi[kpi]
    return formated_result


def process_kpi(list_kpi: List[str],
                kpi_functions: dict,
                cube_loader: Callable[[List[str]], dict],
                filters: dict,
                filters_to_cube_colname: dict = {},
                filters_to_cube_values: dict = {},
                front_filters: dict = {},
                date_format: str = "%d-%m-%Y",
                external_calcul_functions: dict = None,
                comparaison_previous_period: bool = False,
                format_result: bool = False) -> dict:
    """Return the calculation of all the KPIs from list_kpi
    Parameters
    ----------
    list_kpi : List[str]
        the list of KPI to calculate
    kpi_functions : dict
        the definition of each kpi (how to process it)
    cube_loader : Callable[[List[str]], dict]
        a callback to load a list of cube
    filters : dict
        the filters use to filter the cubes
    filters_to_cube_colname : dict, optional
        use to transform a filter key to a cube column name, by default {}
    filters_to_cube_values : dict, optional
        use to transform a filter value to a cube column value, by default {}
    front_filters : dict, optional
        the specific filter use for some of the kpi only, by default {}
    date_format : str, optional
        the date format, by default "%d-%m-%Y"
    external_calcul_functions : dict, optional
        specific calcul fonction to add to the default ones, by default None
    comparaison_previous_period : bool, optional
        True to process the comparaison with the previous period, by default False
    format_result : bool, optional
        True to format the output in a json serialisable way, by default False

    Returns
    -------
    dict
        the result for each kpi (or the encountered errors)
    """

    valid_kpi, error_kpi, loaded_cubes, valid_cubes, _, _ = get_all_valid_kpi_and_cubes(list_kpi,
                                                                                        kpi_functions,
                                                                                        cube_loader)
    filtered_cubes = get_filtered_cubes(filters,
                                        valid_cubes,
                                        loaded_cubes,
                                        date_format,
                                        filters_to_cube_colname,
                                        filters_to_cube_values)

    # Get kpi result for all type of KPI
    result_kpi = get_all_kpi(
        valid_kpi,
        kpi_functions,
        front_filters,
        filtered_cubes,
        external_calcul_functions
    )

    for kpi in error_kpi:
        result_kpi[kpi] = error_kpi[kpi]

    if comparaison_previous_period:
        previous_result = get_kpi_for_previous_period(valid_kpi,
                                                      kpi_functions,
                                                      loaded_cubes,
                                                      filters,
                                                      front_filters,
                                                      external_calcul_functions,
                                                      date_format)

        result_kpi = add_comparaison_to_result(result_kpi, previous_result, kpi_functions)

    return format_kpi_result(result_kpi, kpi_functions) if format_result else result_kpi
