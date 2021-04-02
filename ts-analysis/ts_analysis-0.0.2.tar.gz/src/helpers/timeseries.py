import pandas as pd
import typing


def get_full_index_for_padding(ts_list:typing.List[pd.DataFrame]) -> typing.List[typing.Union[int,float]]:
    """
    Takes in a list of pandas dataframes with timestamps for indexes.
    Returns a list of timestamps to use for a union of all timeseries.
    
    Useful for functions like "pad_out_data".
    """

    full_index = []
    for ts in ts_list:
        full_index = full_index + ts.index.to_list()

    # remove dups
    full_index_no_dups = []
    for x in full_index:
        if x not in full_index_no_dups:
            full_index_no_dups.append(x)

    # sort
    full_index_no_dups.sort()
    return full_index_no_dups
    
    
def pad_out_data(ts_list:typing.List[pd.DataFrame], full_index:typing.List[typing.Union[int,float]], fill_vals={})->typing.List[pd.DataFrame]:
    """
    Takes in list of pandas dataframes with timestamps for indexes.
    Pads out all timeseries to be of equal length with data points
    for all points in the "full_index".

    For timeseries that lack data points for all steps in "full_index",
    fill values are used, as specficed by the fill_vals dict of:
    df_column_name -> fill value (e.g. 0, 0.0). If no "fill_vals" dict
    is given, values are filled in by pandas with NaN.
    
    Returns list of pandas dataframes with padded out timeseries.
    """
    
    padded_dfs = []
    
    for df in ts_list:
        # Get rid of any duplicate time stamps
        df = df[~df.index.duplicated()]
    
        # Sort index.
        df = df.reindex(full_index, method=None).sort_index()
        
        for key, val in fill_vals.items():
            df[key] = df[key].fillna(val)
        df['datetime'] = pd.to_datetime(df.index,unit='s')
        padded_dfs.append(df)
        
    return padded_dfs
    
