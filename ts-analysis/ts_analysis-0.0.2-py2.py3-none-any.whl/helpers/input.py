import itertools
import pandas as pd
import pyfsdb
import lzma
import bz2
import gzip
import typing


def get_uniq_col_groups(df:pd.DataFrame, group_on:str='key', group_size:int=2, min_required_data_points:int=80)->typing.List:
    """ 
    For a dataframe,this returns a list of tuples giving unique combinations of groups 
    of size "group_size" based on grouping data by "group_on" column.
    
    Column values which do not appear enough times to have more than
    "min_required_data_points" are dropped from the combinations.
    
    This is useful in producing multiple time series from a single timeseries
    dataframe - one timeseries per data with matchig 'group_on' value.
    """
    df2 = df.groupby([group_on]).size().to_frame('size').sort_values('size').reset_index()
    is_long_enough = df2['size'] > min_required_data_points
    long_enough_df = df2[is_long_enough]
    group_list = long_enough_df[group_on].to_list()
    
    # If we're not doing pairs or more,
    # just return the list.
    if group_size < 2:
        return group_list
            
    return list(itertools.combinations(group_list,group_size))

def pandas_sort_and_set_time_index(df:pd.DataFrame, datetime_col_name:str='datetime', unit:str='s')->pd.DataFrame:
    """
    Adds column (default name "datetime") to a dataframe
    that contains translation of a row's index into  
    unix timestamps into datetime format. Index values are untouched.
    Returns modified dataframe.
    """
    df = df.sort_index()
    df[datetime_col_name] = pd.to_datetime(df.index,unit=unit)
    return df

def pandas_from_fsdb_files(filenames:typing.List[str], cols:typing.List[str]=[], col_filter={}, logger=None)->pd.DataFrame:
    """
    Pulls data from fsdb formatted files and returns a single pandas dataframe.    
    
    Useful for when there's a large number of files and we want to filter down what we
    keep as we go. 
    
    cols gives the column names (from the fsdb header) we want to keep.
    
    col_filter gives column names (from the fsdb header) we want to keep but only if
    the row has a specific value for that column.
    """
    frames = [pandas_from_fsdb(f, cols=cols, col_filter=col_filter, logger=logger) for f in filenames]
    df = pd.concat(frames)
    return(df)
    
def pandas_from_fsdb(filename:str, cols:typing.List[str]=[], col_filter={}, compression_type=None, logger=None)->pd.DataFrame:
    fh = decompress_and_open(filename, compression_type=compression_type)

    if logger != None:
        logger.debug("Opening and reading from %s", filename)
    db = pyfsdb.Fsdb(file_handle=fh)

    if logger != None:
        logger.debug("FSDB data has columns: %s", ",".join(db.column_names))
    
    # Let pyfsdb call pandas or deal with in-line comment chars in fsdb data. 
    df = db.get_pandas(error_bad_lines=False, engine='python')
    # For pyfsdb before v 1.1.19:
    #df = pd.read_csv(db.file_handle, sep='\t', comment='#',
    #                               names=db.column_names, engine='python', error_bad_lines=False)
    
    # Filter down rows we want to keep.
    # For now - simple logic of == (no other operands/logic)
    # and all values are AND'ed together.
    if logger != None:
        logger.debug("Size of data frame before filtering: %d", len(df))

    for key, value in col_filter.items():
        if logger != None:
            logger.debug("Keeping columns which have %s == %s", key,str(value))
        df = df.loc[df[key] == value]
    if logger != None:
        logger.debug("Size after key value filtering: %d", len(df))

    if logger != None:
        logger.debug("Size of df before col drops: %d", len(df))
    
    if cols:
        headers = df.head()
        for col in cols:
            if col not in headers:
                # log that a requested column was not found
                if logger != None:
                    logger.debug("Asked for column %s, but col not in data. Data has: %s", col, ",".join(headers)) 
        for header in headers:
            if header not in cols:
                df.drop(header, axis=1, inplace=True) 
                # Log what we dropped
                if logger != None:
                    logger.debug("Dropping %s. Not in requested cols: %s", header, ",".join(cols))
    if logger != None:
        logger.debug("Size of df after col drops: %d", len(df))
    
    return df

def decompress_and_open(filename:str, compression_type:typing.Optional[str])->typing.TextIO:
    """
    Given a specific filename, attempts to guess (or use provided 'gz','xz' and 'bz2' hints) 
    and decompress file data.
    
    Returns file handle.
    """
    filename_extension = filename.split('.')[-1]
    if filename_extension == 'gz' or compression_type == 'gz':
        myopen = gzip.open
    elif filename_extension == 'xz' or compression_type == 'xz':
        myopen = lzma.open
    elif filename_extension == 'bz2' or compression_type == 'bz2':
        myopen = bz2.open
    else:
        myopen = open
    fhandle = myopen(filename, 'rt')
    return fhandle 
    
 