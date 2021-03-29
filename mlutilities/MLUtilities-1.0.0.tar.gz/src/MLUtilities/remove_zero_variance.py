import pandas as pd

class remove_zero_variance:
    def __init__(self,df):
        self.df = df # dataframe containing the feature
        #self.feature = feature 
    def columns(self):
        zero_var_cols = [col for col in self.df.columns if self.df[col].nunique(dropna=False) == 1]
        col_keep = np.array([col for col in self.df.columns if col not in zero_var_cols])
        return zero_var_cols