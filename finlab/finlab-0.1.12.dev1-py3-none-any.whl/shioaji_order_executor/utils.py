import pandas as pd
from pydantic import ValidationError
import logging
import shioaji as sj
import os

# Get an instance of a logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
strategy_pkl_path = os.getenv('STRATEGY_PKL_PATH')
orders_pkl_path = os.getenv('ORDERS_PKL_PATH')

"""
API Settings
"""


def activate_shioaji_api(person_id=None, password=None, ca_path="Sinopac.pfx", ca_password=None):
    person_id = os.getenv('person_id', person_id)
    password = os.getenv('password', password)
    ca_path = os.getenv('ca_path', ca_path)
    ca_password = os.getenv('ca_password', ca_password)
    api = sj.Shioaji()
    api.login(person_id, password)
    api.activate_ca(
        ca_path=ca_path,
        person_id=person_id,
        ca_passwd=ca_password,
    )
    return api


class ShioajiApi:

    def __init__(self, api):
        self.api = api
        self.strategy_pkl_path = os.getenv('STRATEGY_PKL_PATH')
        self.orders_pkl_path = os.getenv('ORDERS_PKL_PATH')


"""
Dataframe Process
"""


def df_combine(df_old, df_new, columns_fill=None):
    if columns_fill is None:
        columns_fill = []
    df_old.reset_index(inplace=False)
    df_old.set_index(df_new.index.names, inplace=True)
    if len(columns_fill) > 0:
        for col in columns_fill:
            df_new[col] = df_old[col]
    df_old = pd.concat([df_old, df_new])
    df_old = df_old[~df_old.index.duplicated(keep='last')]
    df_old = df_old.sort_index()
    return df_old


def update_df(model, new_post: dict, df_old=None, columns_fill=None):
    if columns_fill is None:
        columns_fill = []
    try:
        df_new = model(**new_post).get_df()
        if df_old is not None:
            df_new = df_combine(df_old, df_new, columns_fill)
        df_new = df_new.reset_index()
        return df_new
    except ValidationError as e:
        logger.error(e)
        df_new = None
    return df_new


"""
Finance Calculate Function
"""


def cal_profitloss(buy_price, sell_price, num=1, fee=0.001425, tax=0.003):
    profitloss = round((sell_price - buy_price - fee * (buy_price + sell_price) - tax * sell_price) * 1000 * num)
    return profitloss


def get_snapshot(api, stock_list, mode='dict'):
    contracts = [api.Contracts.Stocks.get(code) for code in stock_list]
    market_data = api.snapshots(contracts)
    if mode == 'dict':
        market_data = {snapshot.code: snapshot['close'] for snapshot in market_data}
    elif mode == 'df':
        market_data = pd.DataFrame(market_data)
    return market_data


# init pkl

df_strategy = pd.DataFrame(columns=['name',
                                    'account',
                                    'open_',
                                    'size',
                                    'schedule',
                                    'update_time'])

df_orders = pd.DataFrame(columns=['strategy',
                                  'action',
                                  'cancel_quantity',
                                  'category',
                                  'code',
                                  'deal_quantity',
                                  'exchange',
                                  'modified_price',
                                  'modified_time',
                                  'name',
                                  'order_datetime',
                                  'order_type',
                                  'ordno',
                                  'price',
                                  'price_type',
                                  'quantity',
                                  'reference',
                                  'seqno',
                                  'status',
                                  'status_code',
                                  'deals'])
