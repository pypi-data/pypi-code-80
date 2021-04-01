import pandas as pd
import numpy as np
import datetime


def df_a_day(self):  # return a dataframe with number of bike per day
    last_count = self.iloc[-1, 3]
    velo = self.drop_duplicates('Date')
    time_improved = pd.to_datetime(velo['Date'],
                                   format='%d/%m/%Y')
    velo['Date'] = time_improved
    del velo['Heure / Time']
    velo_ts = velo.set_index(np.arange(len(velo['Date'])))
    df1 = velo_ts['Vélos depuis le 1er janvier / '
                  'Grand total'] - velo_ts["""Vélos ce jour / Today's total"""]
    del df1[0]
    df1.index = np.arange(len(df1))
    i = 1
    while df1[i] > 0:
        df1[i] = df1[i] - df1[0:i].sum()
        i += 1
    df1[i] = 566  # use the real count at 2020-12-31 find at open data mtp
    j = i+2
    for k in range(j, len(df1)):
        df1[k] = df1[k] - df1[j-1:k].sum()
    df1[len(df1)] = last_count
    df1.index = pd.date_range(datetime.date(2020, 3, 12),
                              periods=len(df1))
    return df1.to_frame()


def formatedweek(df):  # add weekday and weed to the data frame
    df.index = pd.date_range(datetime.date(2020, 3, 12),
                             periods=len(df))
    df['weekday'] = df.index.weekday
    df['week'] = df.index.week
    # set weeks starts from first data don't reset at new year
    x = [0 for i in range(4)]
    for i in range(1, (len(df)-4) // 7+1):
        for j in range(7):
            x.append(i)
    for i in range((len(df)-4) % 7):
        x.append((len(df)-4)//7+1)
    df.index = x
    df['week'] = x
    return df


def df_new_year(df):  # only keep data from 2021 of a df_a_day data frame
    df = df.iloc[295:, :]
    df.index = pd.date_range(datetime.date(2021, 1, 1),
                             periods=len(df))
    return df
