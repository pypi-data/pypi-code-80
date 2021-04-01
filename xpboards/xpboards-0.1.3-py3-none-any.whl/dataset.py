import csv
import json
from uuid import uuid4

class XPBoardsDataSet:
    def __init__(self, dataset, convert_types=False):
        """
            The dataset must have the following pattern:

            {
                "id": <integer>, (for XPBoards datasets that already exists, optional)
                "name": <string>,
                "columns":[
                    {
                        "type": <string>,
                        "name": <string>
                    }   
                ],
                "rows": [
                    "values": [
                        {
                            "value": <any> (any primitive type)
                        }
                    ]
                ]
            }
        
        """
        self.__id = dataset.get('id', None)
        self.__name = dataset.get('name', '')

        self.__columns = []

        for column in dataset['columns']:
            self.__columns.append(
                self.Column(
                    name=column['name'],
                    value_type=column.get('type', '')
                )
            )

        self.__rows = []

        for row in dataset['rows']:

            rows = []

            for i in range(len(self.__columns)):

                value = row['values'][i]['value']

                if convert_types:

                    rows.append(
                        self.Row.convert(
                            value=value,
                            to_type=self.__columns[i].value_type
                        )
                    )
                else:
                    rows.append(value)

            self.__rows.append(
                self.Row(
                    values = rows
                )
            )

    # Private

    # Static

    @staticmethod 
    def __parse_dict(data_dict):
        
        columns = []
        rows = []
        item_count = 0

        for row in data_dict:
            
            row_values = []

            for key, value in row.items():
                
                if item_count == 0:
                    columns.append({
                        'name':key,
                        'value_type': None
                    })

                row_values.append({'value':value})

            rows.append({
                'values': row_values
            })

            item_count += 1

        return XPBoardsDataSet({
            'columns':columns,
            'rows': rows
        })

    # Instance

    def __parse_to_dict(self):
        dataset_json = []

        for row in self.__rows:
            json_row = {}

            for i in range(self.columns_count):
                json_row[self.__columns[i].name] = row.values[i]

            dataset_json.append(json_row)

        return dataset_json

    # Public

    # Properties

    @property
    def id(self):
        """
            Returns the dataset id
        """

        return self.__id

    @property
    def columns_count(self):
        """
            Returns the number of columns in the dataset
        """

        return len(self.__columns)

    @property
    def items_count(self):
        """
            Returns the number of rows in the dataset
        """

        return len(self.__rows)

    @property
    def columns(self):
        """
            Returns the list of columns of the dataset
        """

        return self.__columns

    @property
    def items(self):
        """
            Returns the list of rows of the dataset (matrix shape)
        """

        return self.__rows

    @property
    def shape(self):

        """
            Returns the rows X columns of the dataset in a tuple
        """

        return self.items_count, self.columns_count

    @property
    def name(self):
        """
            Returns the dataset name
        """

        return self.__name

    @name.setter
    def name(self, value):
        """
            Sets the name of the dataset
        """

        self.__name = value
  
    # Static

    # @staticmethod
    # def from_csv(path, delimiter=','):
    #     """
    #         Returns a new XPBoardsDataSet instance reading from specified CSV file
    #     """

    #     columns = []
    #     rows = []

    #     with open(path) as csv_file:
    #         reader = csv.reader(csv_file, delimiter=delimiter)

    #         row_count = 0

    #         for row in reader:
    #             if row_count == 0:
    #                 for column in row:

    #                     column_dict = {
    #                         'type': None,
    #                         'name': column
    #                     }

    #                     columns.append(column_dict)
    #             else:
    #                 row_dict = {
    #                     'values': list(map(lambda item: { 'value': item }, row))
    #                 }

    #                 rows.append(row_dict)

    #             row_count += 1


    #     return XPBoardsDataSet({
    #         "columns": columns,
    #         "rows" : rows
    #     })

    @staticmethod
    def read_dict(data):
        """
            Returns a new XPBoardsDataSet instance from a "data" dictionary param.

            The expected dictonary format is the same as pandas dataframe.to_json('records') output.
            Example:
                [
                    {
                        "Name":"Max",
                        "Age": "32"
                    },
                    {
                        "Name":"Scarlett",
                        "Age": "25"
                    }
                ]

        """

        return XPBoardsDataSet.__parse_dict(data)

    @staticmethod
    def read_json(path):
        """
            Returns a new XPBoardsDataSet instance from a JSON file from provided "path" param

            The expected JSON format is the same as pandas dataframe.to_json('records') output.
            Example:
                [
                    {
                        "Name":"Max",
                        "Age": "32"
                    },
                    {
                        "Name":"Scarlett",
                        "Age": "25"
                    }
                ]

        """

        
        data_dict = None

        with open(path) as json_file:
            data_dict = json.load(json_file)

        return XPBoardsDataSet.__parse_dict(data_dict)

    # Instance

    def to_csv(self, path, delimiter=',', quotechar='"'):
        """ 
            Outputs dataset to a CSV file given a path ('path' param)
        """

        with open(path, mode='w') as csv_file:
            
            writer = csv.writer(csv_file, delimiter=delimiter, quotechar=quotechar)
            writer.writerow(self.columns)
            
            for row in self.__rows:
                writer.writerow(row.values)
    
    def to_json(self, path):
        """ 
            Outputs the dataset to a JSON file given a path ('path' param)
        """
        dataset_json = self.__parse_to_dict()

        with open(path, 'w') as f:
            json.dump(dataset_json, f)
    
    def to_dict(self):
        """ 
            Returns the dataset as a python list of dicts
        """

        return self.__parse_to_dict()

    def to_api(self):

        columns = list(map(
            lambda column: {
                    'name': column.name,
                    'type': None if column.value_type == "" else column.value_type
                }, self.__columns))

        rows = list(map(
            lambda row: row.values, self.__rows
        ))

        return ({
            'name': self.name,
            'columns': columns,
            'rows': rows
        })

    def append_item(self, values):
        """ 
            Append item to the end of the dataset, with given array of values
        """
        self.__rows.append(
            self.Row(
                values=values
            )
        )

    def remove_item(self, item_index):
        """ 
            Remove specified item from the dataset
        """
        self.__rows.pop(item_index)

    def append_column(self, name, value_type='text', default_value=''):
        """ 
            Append a column to the end of all columns, setting a default value and type for all items in the dataset
        """
        self.__columns.append(
            self.Column(name=name, value_type=name)
        )

        for row in self.__rows:
            row.values.append(default_value)

    def edit_column(self, column_index, name=None, value_type=None):
        """ 
            Edit specified column with value and value_type
        """
        self.__columns[column_index].value_type = (
            value_type if value_type else self.__columns[column_index].value_type
        )

        self.__columns[column_index].name = (
            name if name else self.__columns[column_index].name
        )
    
    def remove_column(self, column_index):
        """ 
            Remove specified column from the dataset
        """
        self.__columns.pop(column_index)
        for row in self.__rows:
            row.values.pop(column_index)

    # Child Classes

    class ColumnTypes:
        DECIMAL = 'decimal'
        INTEGER = 'integer'
        PERCENTAGE = 'percentage'
        DATE = 'date'
        DATETIME = 'datetime'
        TIME = 'time'
        TEXT = 'text'
        BOOLEAN = 'boolean'

    class Column:
        def __init__(self, name, value_type):
            self.__name = name
            self.__value_type = value_type
            self.__id = uuid4().hex
        
        @property
        def id(self):
            return self.__id

        def __repr__(self):
            return self.__name

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, value):
            self.__name = value

        @property
        def value_type(self):
            return self.__value_type

        @value_type.setter
        def value_type(self, value):
            self.__value_type = value

    class Row:
        def __init__(self, values):
            self.__values = values
            self.__id = uuid4().hex
        
        @property
        def id(self):
            return self.__id

        @property
        def values(self):
            return self.__values

        @values.setter
        def values(self, value):
            self.__values = value

        @staticmethod
        def convert(value, to_type):
            types_converter = {}
            types_converter[XPBoardsDataSet.ColumnTypes.DECIMAL] = lambda x: float(x)
            types_converter[XPBoardsDataSet.ColumnTypes.INTEGER] = lambda x: int(x)
            types_converter[XPBoardsDataSet.ColumnTypes.PERCENTAGE] = lambda x: str(x)
            types_converter[XPBoardsDataSet.ColumnTypes.DATE] = lambda x: str(x)
            types_converter[XPBoardsDataSet.ColumnTypes.DATETIME] = lambda x: str(x)
            types_converter[XPBoardsDataSet.ColumnTypes.TIME] = lambda x: str(x)
            types_converter[XPBoardsDataSet.ColumnTypes.TEXT] = lambda x: str(x)
            types_converter[XPBoardsDataSet.ColumnTypes.BOOLEAN] = lambda x: bool(x)

            try:
                return types_converter[to_type](value)
            except (ValueError, KeyError):
                print(f'Cannot convert {value} to {to_type}, falling back to {XPBoardsDataSet.ColumnTypes.TEXT}')
                return types_converter[XPBoardsDataSet.ColumnTypes.TEXT](value)
        