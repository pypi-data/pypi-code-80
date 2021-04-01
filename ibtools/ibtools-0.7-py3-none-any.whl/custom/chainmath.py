import pandas as pd
import numpy as np
from scipy import stats
from sklearn import preprocessing


def strikesInSd(df, sd):
    return df[(np.abs(stats.zscore(df['strike'])) < sd)]


def normalize(df, range):
    view = df.drop(columns=['strike'])
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=range)
    x_scaled = min_max_scaler.fit_transform(view)
    dataset = pd.DataFrame(x_scaled, columns=view.columns)
    dataset.insert(loc=0, column='strike', value=df['strike'])
    return dataset
