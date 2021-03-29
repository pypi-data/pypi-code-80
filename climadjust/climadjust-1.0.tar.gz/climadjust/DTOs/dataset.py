from enum import Enum
import json


class FormatEnum(Enum):
    NETCDF = "NETCDF"
    VALUE_TEXT = "VALUE_TEXT"


class DatasetDTO:
    def __init__(self, name: str):
        self.name = name

    def get_dict(self):
        d = self.__dict__.copy()
        for key in self.__dict__.keys():
            old_value = d.pop(key)
            if old_value is not None:
                d[key.replace('_DatasetDTO__', '')] = old_value
        return d


class VariableDTO:
    VALID_VARIABLES = ['tas', 'tasmax', 'tasmin', 'pr', 'sfcWind']
    VALID_UNITS = {
        'tas': ['Celsius', 'Kelvin', 'Fahrenheit'],
        'tasmax': ['Celsius', 'Kelvin', 'Fahrenheit'],
        'tasmin':  ['Celsius', 'Kelvin', 'Fahrenheit'],
        'pr': ['mm day-1', 'mm s-1', 'kg m-2 day-1', 'kg m-2', 'mm'],
        'sfcWind': ['m s-1', 'km h-1', 'knots', 'kts', 'mph (nautical miles per hour)']
    }

    def __init__(self, standard_name: str = '', custom_name: str = '',
                 standard_unit: str = '', custom_unit: str = ''):
        self.standardName = standard_name
        self.customName = custom_name
        self.standardUnit = standard_unit
        self.customUnit = custom_unit

    def get_dict(self):
        d = self.__dict__.copy()
        for key, value in self.__dict__.items():
            if value is None:
                d.pop(key)
        return d


def get_variables_dict(variablesDTO: list) -> list:
    return [v.get_dict() for v in variablesDTO]


def to_variableDTO(d: dict) -> VariableDTO:
    dto = VariableDTO()
    if d['standardName'] not in dto.VALID_VARIABLES:
        raise Exception(f"{d['standardName']} is an invalid standard variable")
    dto.standardName = d['standardName']
    dto.customName = d['customName'] if d['customName'] is not None else d['standardName']
    if d['standardUnit'] not in dto.VALID_UNITS[d['standardName']]:
        raise Exception(f"{d['standardUnit']} is an invalid standard unit")
    dto.standardUnit = d['standardUnit']
    dto.customUnit = d['customUnit'] if d['customUnit'] is not None else d['standardUnit']
    return dto


def to_variableDTO_list(var_list: list) -> list:
    return [to_variableDTO(d) for d in var_list]


class InsertDatasetDTO(DatasetDTO):
    """  dataset object with more fields for the upload """

    def __init__(self, name: str, ds_format: str, variables: list):
        DatasetDTO.__init__(self, name)
        try:
            self.format = FormatEnum(ds_format).value
        except ValueError:
            raise Exception("Invalid dataset format. Format is either NETCDF or VALUE_TEXT")
        self.variables = to_variableDTO_list(variables)

    def get_dict(self):
        d = self.__dict__.copy()
        for key, value in self.__dict__.items():
            if value is None:
                d.pop(key)
        # Variables dict
        d['variables'] = json.dumps(get_variables_dict(d['variables']))
        return d




