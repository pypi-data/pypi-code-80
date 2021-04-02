import typing 
import logging

from helpers.input import pandas_from_fsdb_files, pandas_sort_and_set_time_index, get_uniq_col_groups
from baseClasses import InputMixIn

class FSDB2DFnGroups(InputMixIn):

    input_intermediary = None
    group_size = 1
    min_required_data_points = 30
    expected_cols = []
    col_filter = {}
    group_on_key=''
    
    # Config functions.
    def set_filenames(self, filenames:typing.Dict):
        self.filenames = filenames
        
    def set_col_filter(self, col_filter:typing.Dict):
        self.col_filter = col_filter

    def set_expected_cols(self, expected_cols:typing.List):
        self.expected_cols = expected_cols

    def set_min_data_points(self, min_points:int):
        self.min_required_data_points = min_points
    
    def set_group_on_key(self, key:str):
        self.group_on_key = key
    
    def set_group_size(self, size:int):
        self.group_size = size
    
    def set_min_requested_data_points(self, min_points):
        self.min_required_data_points = min_required_data_points
    
    # Main
    def pull_input(self):
        self.logger.debug('Pulling from files: %s', " ".join(self.filenames))
        df = pandas_from_fsdb_files(self.filenames, cols=self.expected_cols, col_filter=self.col_filter, logger=self.logger)
        df.astype({'timestamp':'int'}).dtypes
        df = df.set_index('timestamp')
        df = self._pandas_sort_and_set_time_index(df)
        
        group_list = []
        if self.group_size > 0:
            group_list = get_uniq_col_groups(df, group_on=self.group_on_key, group_size=self.group_size, min_required_data_points=self.min_required_data_points)
        else:
            self.group_list = []
            self.group_on_key = None
        
        self.input_intermediary = (df, group_list, self.group_on_key, self.group_size)
        
    
