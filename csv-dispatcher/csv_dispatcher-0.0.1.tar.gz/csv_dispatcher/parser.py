import pandas as pd


def df_map(foo, dataframe, grouping_columns=[], list_columns=[]):
    if len(grouping_columns):
        columns_to_be_dropped = set(dataframe.columns) - set(list_columns) - set(grouping_columns)
        for group, group_data in dataframe.groupby(grouping_columns):
            non_list_args = group_data[columns_to_be_dropped].drop_duplicates()
            assert len(non_list_args) == 1, "Some values repeat multiple times within a group but ain't a list argument to 'foo': fix the input!."
            kwds = {**non_list_args.to_dict(orient="records")[0],
                    **{name:list(col) for name, col in group_data[list_columns].to_dict(orient="series").items()}}
            foo(**kwds)
    else:
        for index,row in dataframe.iterrows():
            print(dict(row))

def df2kwds_iter(dataframe, list_columns=[], grouping_columns=[]):
    if grouping_columns:
        nonlist_cols = set(dataframe.columns)-set(list_columns)
        scalar_kwds = dataframe[nonlist_cols].drop_duplicates().set_index(grouping_columns)
        list_kwds = dataframe.groupby(grouping_columns)[list_columns].agg(list)
        kwds_df = pd.concat([scalar_kwds, list_kwds], axis=1)
        for group, row in kwds_df.iterrows():
            yield group, dict(row)
    else:
        for group, row in dataframe.iterrows():
            yield group, dict(row)


def removeNAs(as_scalar=True):
    def _removeNAs(x):
        res = list(x.dropna())
        if as_scalar and len(res) == 1:
            return res[0]
        else:
            return res
    return _removeNAs


def df2kwds_iter2(df, grouping_columns=[], as_scalar=True):
    wide_df = df.groupby(grouping_columns).agg(removeNAs(as_scalar)) if grouping_columns else df
    for group, row in wide_df.iterrows():
        yield group, dict(row)
