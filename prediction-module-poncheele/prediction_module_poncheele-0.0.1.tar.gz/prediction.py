import prediction_module as pmd
import pmdarima as pm
import pandas as pd
import datetime
import numpy as np

# Load data
df = pmd.Load_db_predict().save_as_df()
df_day = pmd.df_a_day(df).iloc[:-1, ]

# Seasonal - fit stepwise auto-ARIMA
smodel = pm.auto_arima(df_day[0], start_p=1, start_q=1,
                       test='adf',
                       max_p=5, max_q=5, m=7,
                       start_P=0, seasonal=True,
                       d=None, D=1, trace=True,
                       error_action='ignore',
                       suppress_warnings=True,
                       stepwise=True)

smodel.summary()

# Forcast
n_periods = 2
fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)
index_of_fc = pd.date_range(pd.to_datetime(df.index[-1]) +
                            datetime.timedelta(days=1),
                            periods=n_periods)

# 9oclock proportion
prop_9 = [455.0/1906.0,	318.0/1970.0, 344.0/1580.0,
          358.0/1696.0, 371.0/1891.0, 364.0/1945.0]

print("My prediction :", round(fitted[1] * np.median(np.array(prop_9) * 0.95)))
